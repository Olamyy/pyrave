import os
import requests
import json
from pyrave import __version__
from pyrave.errors import AuthKeyError, HttpMethodError
from pyrave.funcs import is_valid_json


class BaseRaveAPI(object):
    """

    """

    _content_type = "application/json"
    _base_url = {
        "test": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/flwv3-pug/",
        "live": "https://api.ravepay.co/"
    }
    test_encryption_url = "https://ravecrypt.herokuapp.com/rave/encrypt"
    live_encryption_url = ""
    payment_endpoint = "getpaidx/api/"
    disbursement_endpoint = "merchant/disburse"
    recurring_transaction_endpoint = "merchant/subscriptions/"
    refund_transaction_endpoint = "merchant/refund/"
    _docs_url = ""

    def __init__(self, implementation="test"):
        self.public_key = os.getenv("RAVE_PUBLIC_KEY", None)
        self.secret_key = os.getenv("RAVE_SECRET_KEY", None)
        if not self.public_key and not self.secret_key:
            raise AuthKeyError("The secret keys have not been set in your environment. You should get this from your rave "
                               "dashboard and set it in your env. Check {0} for more information".format(self._docs_url))
        self.implementation = implementation

    def _path(self, path):
        url_path = self._base_url.get(self.implementation)
        return url_path + path

    def http_headers(self):
        return {
            "Content-Type": self._content_type,
            "Authorization": "Bearer " + self.secret_key,
            "user-agent": "pyrave-{}".format(__version__)
        }

    def _json_parser(self, json_response):
        """Only the status code, the status of the request and the data
        is sent back. the message is irrelevant if ths request was successful"""
        response = json_response.json()
        status = response.get('status', None)
        message = response.get('message', None)
        data = response.get('data', None)
        if not data:
            return json_response.status_code, json_response
        if message:
            return json_response.status_code, status, data, message
        return json_response.status_code, status, data

    def _exec_request(self, method, url, data=None):
        method_map = {
            'GET': requests.get,
            'POST': requests.post,
        }
        # if not data or is_valid_json(data):
        #     payload = data
        # else:
        #     payload = json.dumps(data)

        # payload = data if is_valid_json(data) or not data else json.dumps(data)
        payload = json.dumps(data) if data else data
        request = method_map.get(method)

        if not request:
            raise HttpMethodError(
                "Request method not recognised or implemented")

        response = request(
            url, headers=self.http_headers(), data=payload, verify=True)
        # print(f"response is {response}")
        print(url)
        if response.status_code == 404:
            if response.json().get('message'):
                body = response.json()
            return response.status_code, body['status'], body['message']
        body = response.json()
        # import pdb; pdb.set_trace()
        print(f"body is {body}")
        if body.get('status') == 'error':
            return response.status_code, body
        if response.status_code in [200, 201]:
            return self._json_parser(response)
        response.raise_for_status()

