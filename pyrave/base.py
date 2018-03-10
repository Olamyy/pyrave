import hashlib
import os
import requests
import json
from pyrave import __version__
from pyrave.errors import AuthKeyError, HttpMethodError


class BaseRaveAPI(object):
    """
        Base PyRave API
    """

    def __init__(self):
        """
        The __init__ method sets some needed defaults.
        """
        self.public_key = os.getenv("RAVE_PUBLIC_KEY", None)
        self.secret_key = os.getenv("RAVE_SECRET_KEY", None)
        self.docs_url = "https://github.com/Olamyy/pyrave/blob/master/README.md"
        if not self.public_key and not self.secret_key:
            raise AuthKeyError("The secret keys have not been set in your environment. You should get this from your rave "
                               "dashboard and set it in your env. Check {0} for more information".format(self.docs_url))
        assert os.environ.get("RAVE_DEBUG"), "The RAVE_DEBUG environment variable should be set. Set it to 1 in test mode and 0 in live mode. " \
                                             "Check {0} for more information".format(self.docs_url)
        self.implementation = "test" if os.environ["RAVE_DEBUG"] == 1 else "live"
        self._content_type = "application/json"
        self._base_url = {
            "test": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/",
            "live": "https://api.ravepay.co/"
        }
        self.rave_url_map = {
            "test_encryption_url": "https://ravecrypt.herokuapp.com/rave/encrypt",
            "live_encryption_url": "",
            "payment_endpoint": self._base_url.get(self.implementation) + "flwv3-pug/getpaidx/api/",
            "disbursement_endpoint": self._base_url.get(self.implementation) + "merchant/disburse",
            "recurring_transaction_endpoint": self._base_url.get(self.implementation) + "merchant/subscriptions",
            "merchant_refund_endpoint": self._base_url.get(self.implementation) + "gpx/merchant/transactions/refund",
        }
        self.encryption_key = self._get_encryption_key()

    def _path(self, path):
        """
        Builds full path given a uri based on the _base_url dict from __init__.
        :param path:
        :return:
        """
        url_path = self._base_url.get(self.implementation)
        return url_path + path

    def _get_encryption_key(self):
        """
        Generates encryption key for user
        :return:
        """
        hashedseckey = hashlib.md5(self.secret_key.encode("utf-8")).hexdigest()
        hashedseckeylast12 = hashedseckey[-12:]
        seckeyadjusted = self.secret_key.replace('FLWSECK-', '')
        seckeyadjustedfirst12 = seckeyadjusted[:12]
        return seckeyadjustedfirst12 + hashedseckeylast12

    def get_url(self, resource=None):
        """
        Retrieve a url from the rave_url_map dict in __init__.
        :param resource:
        :return:
        """
        return self.rave_url_map.get(resource) if resource else self.rave_url_map

    def http_headers(self):
        """
        Setting http headers
        :return:
        """
        return {
            "Content-Type": self._content_type,
            "Authorization": "Bearer " + self.secret_key,
            "user-agent": "pyrave-{}".format(__version__)
        }

    def _json_parser(self, body):
        """Only the status code, the status of the request and the data
        is sent back. the message is irrelevant if ths request was successful"""
        response = body.json()
        status = response.get('status', None)
        message = response.get('message', None)
        data = response.get('data', None)
        if not data or not status or not message:
            return response
        if message:
            return body.status_code, status, data, message
        return body.status_code, status, data

    def _exec_request(self, method, url, data=None, params=False, log_url=False):
        """
        Main HTTP request execution method.
        :param method:
        :param url:
        :param data:
        :param params:
        :param log_url:
        :return:
        """
        method_map = {
            'GET': requests.get,
            'POST': requests.post,
        }
        payload = json.dumps(data) if data else data
        request = method_map.get(method)

        if not request:
            raise HttpMethodError(
                "Request method not recognised or implemented")
        response = request(
            url, headers=self.http_headers(), data=payload, verify=True) if not params else request(
            url, headers=self.http_headers(), params=payload, verify=True)
        if log_url:
            print("The request URL is {}".format(response.url))
        if response.status_code == 404:
            try:
                if response.json():
                    body = response.json()
                    return response.status_code, body['status'], body['message']
                return response.status_code
            except ValueError or json.decoder.JSONDecodeError:
                return response.status_code, "{} returns a 404.".format(url)
        body = response.json()
        if isinstance(body, list):
            return body
        if body.get('status') == 'error':
            return response.status_code, body
        if response.status_code in [200, 201]:
            return self._json_parser(response)
        response.raise_for_status()
