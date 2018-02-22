from pyrave.base import BaseRaveAPI
from pyrave.encryption import RaveEncryption
from pyrave.errors import MissingParamError
from pyrave.utils import generate_id


class Payment(BaseRaveAPI):
    def __init__(self):
        super(Payment, self).__init__()

    def pay(self, using="card", preauthorised=False, return_encrypted=False, **kwargs):
        """

        :param using:
        :param preauthorised:
        :param kwargs:
        :param return_encrypted:
        :return:
        """
        rave_enc = RaveEncryption()
        endpoint = self.payment_endpoint + "charge"
        # for i,v in kwargs.items():
        #     print(f"{i} : {v}")
        if not kwargs.get("txRef"):
            kwargs["txRef"] = generate_id("txRef")
        if not kwargs.get("device_fingerprint"):
            kwargs["device_fingerprint"] = generate_id("device_fingerprint")
        encrypted_data = rave_enc.encrypt(using, preauthorised, **kwargs)
        if return_encrypted:
            return encrypted_data
        url = self._path(endpoint)
        request_data = encrypted_data
        suggested_auth_request = self._exec_request("POST", url, request_data)
        if suggested_auth_request[0] in [400, 401]:
            return suggested_auth_request
        suggested_auth = suggested_auth_request[2].get("suggested_auth")
        if not suggested_auth:
            return suggested_auth_request
        if not kwargs.get("pin"):
                raise MissingParamError("You need to set the pin parameter in the function call "
                                        "to make a payment")
        request_data["suggested_auth"] = suggested_auth
        return self._exec_request("POST", url, request_data)

    def get_encrypted_data(self,using="card", preauthorised=False, **kwargs):
        """

        :param using:
        :param preauthorised:
        :param kwargs:
        :return:
        """
        rave_enc = RaveEncryption()
        return rave_enc.encrypt(using, preauthorised, **kwargs)

    def validate_charge(self, reference, otp, method="card"):
        """

        :param reference:
        :param otp:
        :param method:
        :return:
        """
        request_data = {
            "PBFPubKey": self.secret_key,
            "otp": otp
        }
        endpoint = self.payment_endpoint + "validatecharge" if method == "card" else self.payment_endpoint + "validate"
        request_data.update({"transaction_reference": reference}) if method == "card" else request_data.update({"transactionreference": reference})
        url = self._path(endpoint)
        return self._exec_request("POST", url, request_data)

    def verify_transaction(self, reference, normalize="1"):
        """

        :param reference:
        :param normalize:
        :return:
        """
        endpoint = self.payment_endpoint + "verify"
        request_data = {
            "flw_ref": reference,
            "SECKEY": self.secret_key,
            "normalize": normalize
        }
        url = self._path(endpoint)
        return self._exec_request("POST", url, request_data)

    def disburse(self, bank_code, account_number, currency, amount):
        """
        :param bank_code:
        :param account_number:
        :param currency:
        :param amount:
        :return:
        """
        request_data = {
                "bank_code": bank_code,
                "account_number": account_number,
                "currency": currency,
                "amount": amount,
                "seckey": self.secret_key
        }
        url = self._path(self.disbursement_endpoint)
        return self._exec_request("POST", url, request_data)

    def tokenize_charge(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        endpoint = self.payment_endpoint + "tokenized/charge"
        url = self._path(endpoint)
        return self._exec_request("POST", url, kwargs)

    def refund(self, reference_id):
        endpoint = self.refund_transaction_endpoint + "refund"
        request_data = {
                "ref": reference_id,
                "SECKEY": self.secret_key
        }
        url = self._path(endpoint)
        return self._exec_request("POST", url, request_data)



import os
os.environ["RAVE_SECRET_KEY"] = "FLWSECK-cb26302f4cedae0fdbed8eff3f8279ec-X"
os.environ["RAVE_PUBLIC_KEY"] = "FLWPUBK-7d2b1d0a7b3f48e30299dfa251448491-X"


rave_payment = Payment()
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
    "device_fingerprint": "derjfio32434iojfd",
    "cardno": "5438898014560229",
    "ccv": "789",
    "expirymonth": "09",
    "expiryyear": "19",
    "pin": "3310",

    # 'pin': "3310",
    # "suggested_auth": "PIN"
}
payment = rave_payment.pay(using="card", **data)

print(payment[1])

