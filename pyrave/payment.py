from pyrave.base import BaseRaveAPI
from pyrave.encryption import RaveEncryption
from pyrave.errors import MissingParamError
from pyrave.utils import generate_id


class Payment(BaseRaveAPI):
    """
    Payment API
    """
    def __init__(self):
        super(Payment, self).__init__()
        self.rave_enc = RaveEncryption()

    def pay(self, using="card", preauthorised=False, return_encrypted=False, **kwargs):
        """

        :param using:
        :param preauthorised:
        :param kwargs:
        :param return_encrypted:
        :return:
        """
        endpoint = self.payment_endpoint + "charge"
        if not kwargs.get("txRef"):
            kwargs["txRef"] = generate_id("txRef")
        if not kwargs.get("device_fingerprint"):
            kwargs["device_fingerprint"] = generate_id("device_fingerprint")
        encrypted_data = self.rave_enc.encrypt(using, preauthorised, **kwargs)
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
        return self.rave_enc.encrypt(using, preauthorised, **kwargs)

    def validate_charge(self, reference, otp, method="card"):
        """

        :param reference:
        :param otp:
        :param method:
        :return:
        """
        request_data = {
            "PBFPubKey": self.public_key,
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
        url = self.disbursement_endpoint
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



