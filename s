

# class MockRequest:
#     def __init__(self, response, status_code=200, **kwargs):
#         self.response = response
#         self.overwrite = False
#         if kwargs.get('overwrite'):
#             self.overwrite = True
#         self.status_code = status_code
#
#     @classmethod
#     def raise_for_status(cls):
#         pass
#
#     def json(self):
#         if self.overwrite:
#             return self.response
#         return {'data': self.response}
#
#
# class TestBaseAPI(TestCase):
#     def test_raise_auth_key(self):
#         if not os.environ.get("RAVE_SECRET_KEY") and not os.environ.get("RAVE_PUBLIC_KEY"):
#             with self.assertRaises(AuthKeyError):
#                 BaseRaveAPI()
#
#     def test_path(self):
#         self.base_url = _base_url
#         self.base_api = BaseRaveAPI(implementation="test")
#         path = rave_url_map.get("payment_endpoint") + "charge"
#         self.assertEqual(
#             path, self.base_url[self.base_api.implementation] + "flwv3-pug/getpaidx/api/charge")
#
#
# class TestPay(TestCase):
#     def setUp(self):
#         self.mock_post_patcher = patch('pyrave.base.requests.post')
#         self.mock_post = self.mock_post_patcher.start()
#
#     def tearDown(self):
#         self.mock_post_patcher.stop()
#
#     def test_get_pin(self):
#         self.mock_post.return_value.ok = True
#         data = {
#             "currency": "NGN",
#             "country": "Nigeria",
#             "amount": 5000,
#             "email": "olamyy53@gmail.com",
#             "phonenumber": "09036671876",
#             "firstname": "Lekan",
#             "lastname": "Wahab",
#             "IP": "127.0.0.1",
#             "txRef": "123r34",
#             "accountnumber": "123433453323",
#             "accountbank": "ZENITH BANK PLC",
#             "payment_type": "account"
#         }
#         self.mock_post.return_value = MagicMock()
#         self.mock_post.return_value.json.return_value = data
#
#
# class BaseCallTestCase(TestCase):
#     def setUp(self):
#         self.patcher = patch('pyrave.base.requests.post')
#         self.mock_post = self.patcher.start()
#
#     def tearDown(self):
#         self.patcher.stop()
#
#     def mock_response(self, data, **kwargs):
#         return MockRequest(data, **kwargs)
#
#
# class TestPayment(BaseCallTestCase):
#     def setUp(self):
#         super().setUp()
#         self.base = Payment()
#
#     def test_pay_with_card(self):
#         data = {
#             "currency": "NGN",
#             "country": "Nigeria",
#             "amount": 5000,
#             "email": "olamyy53@gmail.com",
#             "phonenumber": "09036671876",
#             "firstname": "Lekan",
#             "lastname": "Wahab",
#             "IP": "127.0.0.1",
#             "txRef": "123r34",
#             "accountnumber": "123433453323",
#             "accountbank": "ZENITH BANK PLC",
#             "payment_type": "account",
#         }
#
#         self.mock_post.return_value = self.mock_response(
#             {
#                 "status": "success",
#                 "message": "V-COMP",
#                 "data": {
#                     "id": 12945,
#                     "txRef": "MC-7663-YU",
#                     "orderRef": "URF_1501241395442_2906135",
#                     "flwRef": "FLW-MOCK-9deabfa86935b9f0805ae276d49ad079",
#                     "redirectUrl": "http://127.0.0",
#                     "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c",
#                     "settlement_token": None,
#                     "cycle": "one-time",
#                     "amount": 10,
#                     "charged_amount": 10,
#                     "appfee": 0,
#                     "merchantfee": 0,
#                     "merchantbearsfee": 0,
#                     "chargeResponseCode": "02",
#                     "chargeResponseMessage": "Success-Pending-otp-validation",
#                     "authModelUsed": "PIN",
#                     "currency": "NGN",
#                     "IP": "::ffff:127.0.0.1",
#                     "narration": "FLW-PBF CARD Transaction ",
#                     "status": "success-pending-validation",
#                     "vbvrespmessage": "Approved. Successful",
#                     "authurl": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/mockvbvpage?ref=FLW-MOCK-9deabfa86935b9f0805ae276d49ad079&code=00&message=Approved. Successful",
#                     "vbvrespcode": "00",
#                     "acctvalrespmsg": None,
#                     "acctvalrespcode": None,
#                     "paymentType": "card",
#                     "paymentId": "2",
#                     "fraud_status": "ok",
#                     "charge_type": "normal",
#                     "is_live": 0,
#                     "createdAt": "2017-07-28T11:29:55.000Z",
#                     "updatedAt": "2017-07-28T11:29:56.000Z",
#                     "deletedAt": None,
#                     "customerId": 168,
#                     "AccountId": 134,
#                     "customer": {
#                         "id": 168,
#                         "phone": None,
#                         "fullName": "demi adeola",
#                         "customertoken": None,
#                         "email": "tester@flutter.co",
#                         "createdAt": "2017-02-25T12:20:22.000Z",
#                         "updatedAt": "2017-02-25T12:20:22.000Z",
#                         "deletedAt": None,
#                         "AccountId": 134
#                     },
#                     "customercandosubsequentnoauth": "true"
#                 }
#             },
#             overwrite=True,
#             status_code=200
#         )
#         payment = self.base.pay()
#         self.assertEqual(payment[0], 200)
#         self.assertEqual(payment[1], 'success')
#         self.assertEqual(payment[2], data)
#
#     def test_pay_with_account(self):
#         data = {
#             "status": "success",
#             "message": "V-COMP",
#             "data": {
#                 "id": 12945,
#                 "txRef": "MC-7663-YU",
#                 "orderRef": "URF_1501241395442_2906135",
#                 "flwRef": "FLW-MOCK-9deabfa86935b9f0805ae276d49ad079",
#                 "redirectUrl": "http://127.0.0",
#                 "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c",
#                 "settlement_token": None,
#                 "cycle": "one-time",
#                 "amount": 10,
#                 "charged_amount": 10,
#                 "appfee": 0,
#                 "merchantfee": 0,
#                 "merchantbearsfee": 0,
#                 "chargeResponseCode": "02",
#                 "chargeResponseMessage": "Success-Pending-otp-validation",
#                 "authModelUsed": "PIN",
#                 "currency": "NGN",
#                 "IP": "::ffff:127.0.0.1",
#                 "narration": "FLW-PBF CARD Transaction ",
#                 "status": "success-pending-validation",
#                 "vbvrespmessage": "Approved. Successful",
#                 "authurl": "http://flw-pms-dev.eu-west-1.elasticbeanstalk.com/mockvbvpage?ref=FLW-MOCK-9deabfa86935b9f0805ae276d49ad079&code=00&message=Approved. Successful",
#                 "vbvrespcode": "00",
#                 "acctvalrespmsg": None,
#                 "acctvalrespcode": None,
#                 "paymentType": "card",
#                 "paymentId": "2",
#                 "fraud_status": "ok",
#                 "charge_type": "normal",
#                 "is_live": 0,
#                 "createdAt": "2017-07-28T11:29:55.000Z",
#                 "updatedAt": "2017-07-28T11:29:56.000Z",
#                 "deletedAt": None,
#                 "customerId": 168,
#                 "AccountId": 134,
#                 "customer": {
#                     "id": 168,
#                     "phone": None,
#                     "fullName": "demi adeola",
#                     "customertoken": None,
#                     "email": "tester@flutter.co",
#                     "createdAt": "2017-02-25T12:20:22.000Z",
#                     "updatedAt": "2017-02-25T12:20:22.000Z",
#                     "deletedAt": None,
#                     "AccountId": 134
#                 },
#                 "customercandosubsequentnoauth": "true"
#             }
#         }
#
#         self.mock_post.return_value = self.mock_response(
#             {
#                 "currency": "NGN",
#                 "country": "Nigeria",
#                 "amount": 5000,
#                 "email": "olamyy53@gmail.com",
#                 "phonenumber": "09036671876",
#                 "firstname": "Lekan",
#                 "lastname": "Wahab",
#                 "IP": "127.0.0.1",
#                 "txRef": "123r34",
#                 "accountnumber": "123433453323",
#                 "accountbank": "ZENITH BANK PLC",
#                 "payment_type": "account",
#                 'pin': "absc",
#                 "suggested_auth": "pin"
#             }
#             ,
#             overwrite=True,
#             status_code=200
#         )
#         request_data = {
#             "currency": "NGN",
#             "country": "Nigeria",
#             "amount": 5000,
#             "email": "olamyy53@gmail.com",
#             "phonenumber": "09036671876",
#             "firstname": "Lekan",
#             "lastname": "Wahab",
#             "IP": "127.0.0.1",
#             "txRef": "123r34",
#             "accountnumber": "123433453323",
#             "accountbank": "ZENITH BANK PLC",
#             "payment_type": "account",
#             'pin': "absc",
#             "suggested_auth": "pin"
#         }
#         payment = self.base.pay(using="account", **request_data)
#         self.assertEqual(payment[0], 200)
#         self.assertEqual(payment[1].json(), data)
#
#     def test_get_pin(self):
#         data = {
#             "currency": "NGN",
#             "country": "Nigeria",
#             "amount": 5000,
#             "email": "olamyy53@gmail.com",
#             "phonenumber": "09036671876",
#             "firstname": "Lekan",
#             "lastname": "Wahab",
#             "IP": "127.0.0.1",
#             "txRef": "123r34",
#             "accountnumber": "123433453323",
#             "accountbank": "ZENITH BANK PLC",
#             "payment_type": "account"
#         }
#
#         self.mock_post.return_value = self.mock_response(
#             {
#                 "PBFPubKey": "FLWPUBK-e634d14d9ded04eaf05d5b63a0a06d2f-X",
#                 "client": "DqjGqhXGwc3PFxxBAhrTanLdplzwKxGkQPydlxgTgsQKgw9Noe02sN4NZwZXD2/wJc4PtPHJzwNFr16lMLB+qh8oE0b8EiiW8hDilo+Y"
#                           "2mEWBF1dtr6g2oaQI6RoMYoe1Q9UvZv0Y5TdHceeFKDzC++37ed/OoPO8ckBwR0n3SCCahUIaxpeSSmP5/oX4kM/T9mAZji57cpGn6Ub6Oz7"
#                           "96a3P2kWAwzs0/+LZJqSzcdI3dzErf0Qcgx1P6tFDuS2R7vz+mMjKageqQrrbCvNAjjZA1DBDW2Uv0hr1h+Tle4Ew/+Hud1VD+X8CvQGnFHf2"
#                           "DUHm9Y7LAxN6ff8xl7efhP6mmHlXTenCSfvJjALR3d9zmR1XLdpSX5JLB1Cp3CWhX/ZowrgK9auye+1PP1TNPb82aIB8cKGHUdY4KUt7OVaA3vPILo"
#                           "G++brZHuI0YDQJ2DmoLe+mXH5b6GpO7MWi2Lcrg/QTfnQ0ZNcamItOSQscAIdY7f6CrW8EecaC/tUXwb1wp2knauEtcQ3yj0vyIa/ezIxz7zQBdK35UIUCvU=",
#                 "alg": "3DES-24"
#             },
#             overwrite=True,
#             status_code=200
#         )
#         payment = self.base.pay(action="get_pin", preauthorised=False, using="account", **data)
#         self.assertEqual(payment[0], 200)
#
#     def test_validate_charge_with_card(self):
#         pass
#
#     def test_validate_charge_with_account(self):
#         pass
#
#     def test_verify_transaction(self):
#         pass
#
#     def test_disburse(self):
#         pass
#
#     def test_capture_preauthorised_transaction(self):
#         pass
#
#     def test_refund_or_void_transaction(self):
#         pass
#
#     def test_tokenize_charge(self):
#         pass
#
#     def test_refund(self):
#         pass
#
#
# class TestTransaction(BaseCallTestCase):
#     pass
#
#
# class TestEncryption(BaseCallTestCase):
#     pass
#
#
# class TestMisc(BaseCallTestCase):
#     pass