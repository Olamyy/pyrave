import unittest
import os
from unittest import TestCase

from pyrave import RaveEncryption
from pyrave.base import BaseRaveAPI
from pyrave.errors import AuthKeyError

from mock import patch, Mock


class TestConfig(object):
    demo_public_key = "FLWPUBK-7d2b1d0a7b3f48e30299dfa251448491-X"
    demo_secret_key = "FLWSECK-cb26302f4cedae0fdbed8eff3f8279ec-X"

    test_user = {
        "company_name": "Albert Specialist Hospital",
        "first_name": "Albert",
        "last_name": "Jane",
        "email": "jane@alberthospital.com",
        "phone": "+2348012345678",
        "website": "http://www.alberthospital.com",
        "address": "Wase II"
    }


config = TestConfig

_content_type = "application/json"

_base_url = {
    "test": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/",
    "live": "https://api.ravepay.co/"
}

rave_url_map = {
    "test_encryption_url": "https://ravecrypt.herokuapp.com/rave/encrypt",
    "live_encryption_url": "",
    "payment_endpoint": _base_url.get("test") + "flwv3-pug/getpaidx/api/",
    "disbursement_endpoint": _base_url.get("test") + "merchant/disburse",
    "recurring_transaction_endpoint": _base_url.get("test") + "merchant/subscriptions",
    "merchant_refund_endpoint": _base_url.get("test") + "gpx/merchant/transactions/refund",
    "docs_url": "https://github.com/Olamyy/pyrave/blob/master/README.md"
}

os.environ["RAVE_SECRET_KEY"] = "FLWSECK-cb26302f4cedae0fdbed8eff3f8279ec-X"
os.environ["RAVE_PUBLIC_KEY"] = "FLWPUBK-7d2b1d0a7b3f48e30299dfa251448491-X"
os.environ["RAVE_DEBUG"] = "1"


class TestBaseAPI(TestCase):
    def test_raise_auth_key(self):
        if not os.environ.get("RAVE_SECRET_KEY") and not os.environ.get("RAVE_PUBLIC_KEY"):
            with self.assertRaises(AuthKeyError):
                BaseRaveAPI()

    def test_path_live(self):
        self.base_url = _base_url
        self.base_api = BaseRaveAPI()
        path = rave_url_map.get("payment_endpoint") + "charge"
        self.assertEqual(
            path, self.base_url[self.base_api.implementation] + "flwv3-pug/getpaidx/api/charge")

    def test_path_test(self):
        self.base_url = _base_url
        self.base_api = BaseRaveAPI()
        path = rave_url_map.get("payment_endpoint") + "charge"
        self.assertEqual(
            path, self.base_url[self.base_api.implementation] + "flwv3-pug/getpaidx/api/charge")


class TestEncrypt(TestCase):
    data = {
        "currency": "NGN",
        "country": "Nigeria",
        "amount": 5000,
        "email": "olamyy53@gmail.com",
        "phonenumber": "09036671876",
        "firstname": "Lekan",
        "lastname": "Wahab",
        "IP": "127.0.0.1",
        "txRef": "123r34",
        "accountnumber": "123433453323",
        "accountbank": "ZENITH BANK PLC",
        "payment_type": "account"
    }

    @patch('requests.get')
    def test_get_encrypted_data(self, r_post):
        m = RaveEncryption()

        reply = dict(PBFPubKey='FLWPUBK-7d2b1d0a7b3f48e30299dfa251448491-X', alg='3DES-24',
                     client='P86tACtS41M=')
        r_post.return_value.json = Mock(return_value=reply)

        result = m.encrypt(**self.data)
        self.assertEqual(reply, result)


class TestPayment(TestCase):
    @patch('requests.post')
    def test_pay(self):
        pass

    def test_verify_payment(self):
        pass

if __name__ == '__main__':
    unittest.main()
