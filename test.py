import unittest
import os
from unittest import TestCase

from pyrave import RaveEncryption
from pyrave.base import BaseRaveAPI
from pyrave.errors import AuthKeyError
from pyrave.payment import Payment

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


class TestBaseAPI(TestCase):
    def test_raise_auth_key(self):
        if not os.environ.get("RAVE_SECRET_KEY") and not os.environ.get("RAVE_PUBLIC_KEY"):
            with self.assertRaises(AuthKeyError):
                BaseRaveAPI()

    def test_path(self):
        self.base_url = _base_url
        self.base_api = BaseRaveAPI(implementation="test")
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
        """A message can be posted to a channel"""
        m = RaveEncryption()

        reply = dict(PBFPubKey='FLWPUBK-7d2b1d0a7b3f48e30299dfa251448491-X', alg='3DES-24', client='P86tACtS41M=')
        r_post.return_value.json = Mock(return_value=reply)

        result = m.encrypt(**self.data)
        self.assertEqual(reply, result)


class TestPayment(TestCase):
    def setUp(self):
        super(TestPayment, self).setUp()
        self.base = Payment()

    def test_pay_with_card(self):
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
            "payment_type": "account",
        }

        reply = {
                "status": "success",
                "message": "V-COMP",
                "data": {
                    "id": 12945,
                    "txRef": "MC-7663-YU",
                    "orderRef": "URF_1501241395442_2906135",
                    "flwRef": "FLW-MOCK-9deabfa86935b9f0805ae276d49ad079",
                    "redirectUrl": "http://127.0.0",
                    "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c",
                    "settlement_token": None,
                    "cycle": "one-time",
                    "amount": 10,
                    "charged_amount": 10,
                    "appfee": 0,
                    "merchantfee": 0,
                    "merchantbearsfee": 0,
                    "chargeResponseCode": "02",
                    "chargeResponseMessage": "Success-Pending-otp-validation",
                    "authModelUsed": "PIN",
                    "currency": "NGN",
                    "IP": "::ffff:127.0.0.1",
                    "narration": "FLW-PBF CARD Transaction ",
                    "status": "success-pending-validation",
                    "vbvrespmessage": "Approved. Successful",
                    "authurl": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/mockvbvpage?ref=FLW-MOCK-9deabfa86935b9f0805ae276d49ad079&code=00&message=Approved. Successful",
                    "vbvrespcode": "00",
                    "acctvalrespmsg": None,
                    "acctvalrespcode": None,
                    "paymentType": "card",
                    "paymentId": "2",
                    "fraud_status": "ok",
                    "charge_type": "normal",
                    "is_live": 0,
                    "createdAt": "2017-07-28T11:29:55.000Z",
                    "updatedAt": "2017-07-28T11:29:56.000Z",
                    "deletedAt": None,
                    "customerId": 168,
                    "AccountId": 134,
                    "customer": {
                        "id": 168,
                        "phone": None,
                        "fullName": "demi adeola",
                        "customertoken": None,
                        "email": "tester@flutter.co",
                        "createdAt": "2017-02-25T12:20:22.000Z",
                        "updatedAt": "2017-02-25T12:20:22.000Z",
                        "deletedAt": None,
                        "AccountId": 134
                    },
                    "customercandosubsequentnoauth": "true"
                }
            }

        payment = self.base.pay(**data)
        print(payment)
        self.assertEqual(payment[0], 200)
        self.assertEqual(reply, payment)

    def test_pay_with_account(self):
        data = {
            "status": "success",
            "message": "V-COMP",
            "data": {
                "id": 12945,
                "txRef": "MC-7663-YU",
                "orderRef": "URF_1501241395442_2906135",
                "flwRef": "FLW-MOCK-9deabfa86935b9f0805ae276d49ad079",
                "redirectUrl": "http://127.0.0",
                "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c",
                "settlement_token": None,
                "cycle": "one-time",
                "amount": 10,
                "charged_amount": 10,
                "appfee": 0,
                "merchantfee": 0,
                "merchantbearsfee": 0,
                "chargeResponseCode": "02",
                "chargeResponseMessage": "Success-Pending-otp-validation",
                "authModelUsed": "PIN",
                "currency": "NGN",
                "IP": "::ffff:127.0.0.1",
                "narration": "FLW-PBF CARD Transaction ",
                "status": "success-pending-validation",
                "vbvrespmessage": "Approved. Successful",
                "authurl": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/mockvbvpage?ref=FLW-MOCK-9deabfa86935b9f0805ae276d49ad079&code=00&message=Approved. Successful",
                "vbvrespcode": "00",
                "acctvalrespmsg": None,
                "acctvalrespcode": None,
                "paymentType": "card",
                "paymentId": "2",
                "fraud_status": "ok",
                "charge_type": "normal",
                "is_live": 0,
                "createdAt": "2017-07-28T11:29:55.000Z",
                "updatedAt": "2017-07-28T11:29:56.000Z",
                "deletedAt": None,
                "customerId": 168,
                "AccountId": 134,
                "customer": {
                    "id": 168,
                    "phone": None,
                    "fullName": "demi adeola",
                    "customertoken": None,
                    "email": "tester@flutter.co",
                    "createdAt": "2017-02-25T12:20:22.000Z",
                    "updatedAt": "2017-02-25T12:20:22.000Z",
                    "deletedAt": None,
                    "AccountId": 134
                },
                "customercandosubsequentnoauth": "true"
            }
        }

        request_data = {
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
                "payment_type": "account",
                'pin': "absc",
                "suggested_auth": "pin"
            }

        payment = self.base.pay(using="account", **request_data)
        self.assertEqual(payment[0], 200)
        self.assertEqual(payment[1].json(), data)

    def test_validate_charge_with_card(self):
        payment = self.base.validate_charge(otp='otp', reference='')
        self.assertEqual(payment[0], 200)

    def test_validate_charge_with_account(self):
        data = {
            "status": "success",
            "message": "V-COMP",
            "data": {
                "id": 12945,
                "txRef": "MC-7663-YU",
                "orderRef": "URF_1501241395442_2906135",
                "flwRef": "FLW-MOCK-9deabfa86935b9f0805ae276d49ad079",
                "redirectUrl": "http://127.0.0",
                "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c",
                "settlement_token": None,
                "cycle": "one-time",
                "amount": 10,
                "charged_amount": 10,
                "appfee": 0,
                "merchantfee": 0,
                "merchantbearsfee": 0,
                "chargeResponseCode": "02",
                "chargeResponseMessage": "Success-Pending-otp-validation",
                "authModelUsed": "PIN",
                "currency": "NGN",
                "IP": "::ffff:127.0.0.1",
                "narration": "FLW-PBF CARD Transaction ",
                "status": "success-pending-validation",
                "vbvrespmessage": "Approved. Successful",
                "authurl": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/mockvbvpage?ref=FLW-MOCK-9deabfa86935b9f0805ae276d49ad079&code=00&message=Approved. Successful",
                "vbvrespcode": "00",
                "acctvalrespmsg": None,
                "acctvalrespcode": None,
                "paymentType": "card",
                "paymentId": "2",
                "fraud_status": "ok",
                "charge_type": "normal",
                "is_live": 0,
                "createdAt": "2017-07-28T11:29:55.000Z",
                "updatedAt": "2017-07-28T11:29:56.000Z",
                "deletedAt": None,
                "customerId": 168,
                "AccountId": 134,
                "customer": {
                    "id": 168,
                    "phone": None,
                    "fullName": "demi adeola",
                    "customertoken": None,
                    "email": "tester@flutter.co",
                    "createdAt": "2017-02-25T12:20:22.000Z",
                    "updatedAt": "2017-02-25T12:20:22.000Z",
                    "deletedAt": None,
                    "AccountId": 134
                },
                "customercandosubsequentnoauth": "true"
            }
        }

        request_data = {
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
            "payment_type": "account",
            'pin': "absc",
            "suggested_auth": "pin"
        }

        payment = self.base.pay(using="account", **request_data)
        self.assertEqual(payment[0], 200)
        self.assertEqual(payment[1].json(), data)

    def test_verify_transaction(self):
        data = {
            "status": "success",
            "message": "V-COMP",
            "data": {
                "id": 12945,
                "txRef": "MC-7663-YU",
                "orderRef": "URF_1501241395442_2906135",
                "flwRef": "FLW-MOCK-9deabfa86935b9f0805ae276d49ad079",
                "redirectUrl": "http://127.0.0",
                "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c",
                "settlement_token": None,
                "cycle": "one-time",
                "amount": 10,
                "charged_amount": 10,
                "appfee": 0,
                "merchantfee": 0,
                "merchantbearsfee": 0,
                "chargeResponseCode": "02",
                "chargeResponseMessage": "Success-Pending-otp-validation",
                "authModelUsed": "PIN",
                "currency": "NGN",
                "IP": "::ffff:127.0.0.1",
                "narration": "FLW-PBF CARD Transaction ",
                "status": "success-pending-validation",
                "vbvrespmessage": "Approved. Successful",
                "authurl": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/mockvbvpage?ref=FLW-MOCK-9deabfa86935b9f0805ae276d49ad079&code=00&message=Approved. Successful",
                "vbvrespcode": "00",
                "acctvalrespmsg": None,
                "acctvalrespcode": None,
                "paymentType": "card",
                "paymentId": "2",
                "fraud_status": "ok",
                "charge_type": "normal",
                "is_live": 0,
                "createdAt": "2017-07-28T11:29:55.000Z",
                "updatedAt": "2017-07-28T11:29:56.000Z",
                "deletedAt": None,
                "customerId": 168,
                "AccountId": 134,
                "customer": {
                    "id": 168,
                    "phone": None,
                    "fullName": "demi adeola",
                    "customertoken": None,
                    "email": "tester@flutter.co",
                    "createdAt": "2017-02-25T12:20:22.000Z",
                    "updatedAt": "2017-02-25T12:20:22.000Z",
                    "deletedAt": None,
                    "AccountId": 134
                },
                "customercandosubsequentnoauth": "true"
            }
        }

        request_data = {
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
            "payment_type": "account",
            'pin': "absc",
            "suggested_auth": "pin"
        }

        payment = self.base.pay(using="account", **request_data)
        self.assertEqual(payment[0], 200)
        self.assertEqual(payment[1].json(), data)

    def test_disburse(self):
        data = {
            "status": "success",
            "message": "V-COMP",
            "data": {
                "id": 12945,
                "txRef": "MC-7663-YU",
                "orderRef": "URF_1501241395442_2906135",
                "flwRef": "FLW-MOCK-9deabfa86935b9f0805ae276d49ad079",
                "redirectUrl": "http://127.0.0",
                "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c",
                "settlement_token": None,
                "cycle": "one-time",
                "amount": 10,
                "charged_amount": 10,
                "appfee": 0,
                "merchantfee": 0,
                "merchantbearsfee": 0,
                "chargeResponseCode": "02",
                "chargeResponseMessage": "Success-Pending-otp-validation",
                "authModelUsed": "PIN",
                "currency": "NGN",
                "IP": "::ffff:127.0.0.1",
                "narration": "FLW-PBF CARD Transaction ",
                "status": "success-pending-validation",
                "vbvrespmessage": "Approved. Successful",
                "authurl": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/mockvbvpage?ref=FLW-MOCK-9deabfa86935b9f0805ae276d49ad079&code=00&message=Approved. Successful",
                "vbvrespcode": "00",
                "acctvalrespmsg": None,
                "acctvalrespcode": None,
                "paymentType": "card",
                "paymentId": "2",
                "fraud_status": "ok",
                "charge_type": "normal",
                "is_live": 0,
                "createdAt": "2017-07-28T11:29:55.000Z",
                "updatedAt": "2017-07-28T11:29:56.000Z",
                "deletedAt": None,
                "customerId": 168,
                "AccountId": 134,
                "customer": {
                    "id": 168,
                    "phone": None,
                    "fullName": "demi adeola",
                    "customertoken": None,
                    "email": "tester@flutter.co",
                    "createdAt": "2017-02-25T12:20:22.000Z",
                    "updatedAt": "2017-02-25T12:20:22.000Z",
                    "deletedAt": None,
                    "AccountId": 134
                },
                "customercandosubsequentnoauth": "true"
            }
        }

        request_data = {
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
            "payment_type": "account",
            'pin': "absc",
            "suggested_auth": "pin"
        }

        payment = self.base.pay(using="account", **request_data)
        self.assertEqual(payment[0], 200)
        self.assertEqual(payment[1].json(), data)

    def test_capture_preauthorised_transaction(self):
        data = {
            "status": "success",
            "message": "V-COMP",
            "data": {
                "id": 12945,
                "txRef": "MC-7663-YU",
                "orderRef": "URF_1501241395442_2906135",
                "flwRef": "FLW-MOCK-9deabfa86935b9f0805ae276d49ad079",
                "redirectUrl": "http://127.0.0",
                "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c",
                "settlement_token": None,
                "cycle": "one-time",
                "amount": 10,
                "charged_amount": 10,
                "appfee": 0,
                "merchantfee": 0,
                "merchantbearsfee": 0,
                "chargeResponseCode": "02",
                "chargeResponseMessage": "Success-Pending-otp-validation",
                "authModelUsed": "PIN",
                "currency": "NGN",
                "IP": "::ffff:127.0.0.1",
                "narration": "FLW-PBF CARD Transaction ",
                "status": "success-pending-validation",
                "vbvrespmessage": "Approved. Successful",
                "authurl": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/mockvbvpage?ref=FLW-MOCK-9deabfa86935b9f0805ae276d49ad079&code=00&message=Approved. Successful",
                "vbvrespcode": "00",
                "acctvalrespmsg": None,
                "acctvalrespcode": None,
                "paymentType": "card",
                "paymentId": "2",
                "fraud_status": "ok",
                "charge_type": "normal",
                "is_live": 0,
                "createdAt": "2017-07-28T11:29:55.000Z",
                "updatedAt": "2017-07-28T11:29:56.000Z",
                "deletedAt": None,
                "customerId": 168,
                "AccountId": 134,
                "customer": {
                    "id": 168,
                    "phone": None,
                    "fullName": "demi adeola",
                    "customertoken": None,
                    "email": "tester@flutter.co",
                    "createdAt": "2017-02-25T12:20:22.000Z",
                    "updatedAt": "2017-02-25T12:20:22.000Z",
                    "deletedAt": None,
                    "AccountId": 134
                },
                "customercandosubsequentnoauth": "true"
            }
        }

        request_data = {
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
            "payment_type": "account",
            'pin': "absc",
            "suggested_auth": "pin"
        }

        payment = self.base.pay(using="account", **request_data)
        self.assertEqual(payment[0], 200)
        self.assertEqual(payment[1].json(), data)

    def test_refund_or_void_transaction(self):
        data = {
            "status": "success",
            "message": "V-COMP",
            "data": {
                "id": 12945,
                "txRef": "MC-7663-YU",
                "orderRef": "URF_1501241395442_2906135",
                "flwRef": "FLW-MOCK-9deabfa86935b9f0805ae276d49ad079",
                "redirectUrl": "http://127.0.0",
                "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c",
                "settlement_token": None,
                "cycle": "one-time",
                "amount": 10,
                "charged_amount": 10,
                "appfee": 0,
                "merchantfee": 0,
                "merchantbearsfee": 0,
                "chargeResponseCode": "02",
                "chargeResponseMessage": "Success-Pending-otp-validation",
                "authModelUsed": "PIN",
                "currency": "NGN",
                "IP": "::ffff:127.0.0.1",
                "narration": "FLW-PBF CARD Transaction ",
                "status": "success-pending-validation",
                "vbvrespmessage": "Approved. Successful",
                "authurl": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/mockvbvpage?ref=FLW-MOCK-9deabfa86935b9f0805ae276d49ad079&code=00&message=Approved. Successful",
                "vbvrespcode": "00",
                "acctvalrespmsg": None,
                "acctvalrespcode": None,
                "paymentType": "card",
                "paymentId": "2",
                "fraud_status": "ok",
                "charge_type": "normal",
                "is_live": 0,
                "createdAt": "2017-07-28T11:29:55.000Z",
                "updatedAt": "2017-07-28T11:29:56.000Z",
                "deletedAt": None,
                "customerId": 168,
                "AccountId": 134,
                "customer": {
                    "id": 168,
                    "phone": None,
                    "fullName": "demi adeola",
                    "customertoken": None,
                    "email": "tester@flutter.co",
                    "createdAt": "2017-02-25T12:20:22.000Z",
                    "updatedAt": "2017-02-25T12:20:22.000Z",
                    "deletedAt": None,
                    "AccountId": 134
                },
                "customercandosubsequentnoauth": "true"
            }
        }

        request_data = {
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
            "payment_type": "account",
            'pin': "absc",
            "suggested_auth": "pin"
        }

        payment = self.base.pay(using="account", **request_data)
        self.assertEqual(payment[0], 200)
        self.assertEqual(payment[1].json(), data)

    def test_tokenize_charge(self):
        data = {
            "status": "success",
            "message": "V-COMP",
            "data": {
                "id": 12945,
                "txRef": "MC-7663-YU",
                "orderRef": "URF_1501241395442_2906135",
                "flwRef": "FLW-MOCK-9deabfa86935b9f0805ae276d49ad079",
                "redirectUrl": "http://127.0.0",
                "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c",
                "settlement_token": None,
                "cycle": "one-time",
                "amount": 10,
                "charged_amount": 10,
                "appfee": 0,
                "merchantfee": 0,
                "merchantbearsfee": 0,
                "chargeResponseCode": "02",
                "chargeResponseMessage": "Success-Pending-otp-validation",
                "authModelUsed": "PIN",
                "currency": "NGN",
                "IP": "::ffff:127.0.0.1",
                "narration": "FLW-PBF CARD Transaction ",
                "status": "success-pending-validation",
                "vbvrespmessage": "Approved. Successful",
                "authurl": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/mockvbvpage?ref=FLW-MOCK-9deabfa86935b9f0805ae276d49ad079&code=00&message=Approved. Successful",
                "vbvrespcode": "00",
                "acctvalrespmsg": None,
                "acctvalrespcode": None,
                "paymentType": "card",
                "paymentId": "2",
                "fraud_status": "ok",
                "charge_type": "normal",
                "is_live": 0,
                "createdAt": "2017-07-28T11:29:55.000Z",
                "updatedAt": "2017-07-28T11:29:56.000Z",
                "deletedAt": None,
                "customerId": 168,
                "AccountId": 134,
                "customer": {
                    "id": 168,
                    "phone": None,
                    "fullName": "demi adeola",
                    "customertoken": None,
                    "email": "tester@flutter.co",
                    "createdAt": "2017-02-25T12:20:22.000Z",
                    "updatedAt": "2017-02-25T12:20:22.000Z",
                    "deletedAt": None,
                    "AccountId": 134
                },
                "customercandosubsequentnoauth": "true"
            }
        }

        request_data = {
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
            "payment_type": "account",
            'pin': "absc",
            "suggested_auth": "pin"
        }

        payment = self.base.pay(using="account", **request_data)
        self.assertEqual(payment[0], 200)
        self.assertEqual(payment[1].json(), data)

    def test_refund(self):
        data = {
            "status": "success",
            "message": "V-COMP",
            "data": {
                "id": 12945,
                "txRef": "MC-7663-YU",
                "orderRef": "URF_1501241395442_2906135",
                "flwRef": "FLW-MOCK-9deabfa86935b9f0805ae276d49ad079",
                "redirectUrl": "http://127.0.0",
                "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c",
                "settlement_token": None,
                "cycle": "one-time",
                "amount": 10,
                "charged_amount": 10,
                "appfee": 0,
                "merchantfee": 0,
                "merchantbearsfee": 0,
                "chargeResponseCode": "02",
                "chargeResponseMessage": "Success-Pending-otp-validation",
                "authModelUsed": "PIN",
                "currency": "NGN",
                "IP": "::ffff:127.0.0.1",
                "narration": "FLW-PBF CARD Transaction ",
                "status": "success-pending-validation",
                "vbvrespmessage": "Approved. Successful",
                "authurl": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/mockvbvpage?ref=FLW-MOCK-9deabfa86935b9f0805ae276d49ad079&code=00&message=Approved. Successful",
                "vbvrespcode": "00",
                "acctvalrespmsg": None,
                "acctvalrespcode": None,
                "paymentType": "card",
                "paymentId": "2",
                "fraud_status": "ok",
                "charge_type": "normal",
                "is_live": 0,
                "createdAt": "2017-07-28T11:29:55.000Z",
                "updatedAt": "2017-07-28T11:29:56.000Z",
                "deletedAt": None,
                "customerId": 168,
                "AccountId": 134,
                "customer": {
                    "id": 168,
                    "phone": None,
                    "fullName": "demi adeola",
                    "customertoken": None,
                    "email": "tester@flutter.co",
                    "createdAt": "2017-02-25T12:20:22.000Z",
                    "updatedAt": "2017-02-25T12:20:22.000Z",
                    "deletedAt": None,
                    "AccountId": 134
                },
                "customercandosubsequentnoauth": "true"
            }
        }

        request_data = {
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
            "payment_type": "account",
            'pin': "absc",
            "suggested_auth": "pin"
        }

        payment = self.base.pay(using="account", **request_data)
        self.assertEqual(payment[0], 200)
        self.assertEqual(payment[1].json(), data)


if __name__ == '__main__':
    unittest.main()
