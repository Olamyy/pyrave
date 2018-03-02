from pyrave.base import BaseRaveAPI
from pyrave.encryption import RaveEncryption
from pyrave.errors import MissingParamError
from pyrave.utils import generate_id


class Payment(BaseRaveAPI):
    """
    Payment API
    """

    def __init__(self, implementation):
        super(Payment, self).__init__(implementation)
        self.rave_enc = RaveEncryption(implementation)

    def pay(self, using="card", preauthorised=False, return_encrypted=False, log_url=False, **kwargs):
        """

        :param log_url:
        :param using:
        :param preauthorised:
        :param kwargs:
        :param return_encrypted:
        :return:
        """
        if not kwargs.get("txRef"):
            kwargs["txRef"] = generate_id("txRef")
        if not kwargs.get("device_fingerprint"):
            kwargs["device_fingerprint"] = generate_id("device_fingerprint")
        encrypted_data = self.rave_enc.encrypt(using, preauthorised, **kwargs)
        if return_encrypted:
            return encrypted_data
        url = self.rave_url_map.get("payment_endpoint") + "charge"
        print(encrypted_data)
        suggested_auth_request = self._exec_request("POST", url, encrypted_data)
        if suggested_auth_request[0] in [400, 401]:
            return suggested_auth_request
        suggested_auth = suggested_auth_request[2].get("suggested_auth")
        if not suggested_auth:
            return suggested_auth_request
        if not kwargs.get("pin"):
            raise MissingParamError("You need to set the pin parameter in the function call "
                                    "to make a payment")
        encrypted_data["suggested_auth"] = suggested_auth
        return self._exec_request("POST", url, encrypted_data, log_url=log_url)

    def get_encrypted_data(self, using="card", preauthorised=False, log_url=False, **kwargs):
        """

        :param log_url:
        :param using:
        :param preauthorised:
        :param kwargs:
        :return:
        """

        return self.rave_enc.encrypt(using, preauthorised, log_url=log_url, **kwargs)

    def validate_charge(self, reference, otp, method="card", log_url=False, ):
        """

        :param log_url:
        :param reference:
        :param otp:
        :param method:
        :return:
        """
        request_data = {
            "PBFPubKey": self.public_key,
            "otp": otp
        }
        request_data.update({"transaction_reference": reference}) if method == "card" else request_data.update({"transactionreference": reference})
        url = self.rave_url_map.get("payment_endpoint") + "validatecharge" if method == "card" else self.rave_url_map.get("payment_endpoint") + "validate"
        return self._exec_request("POST", url, request_data, log_url=log_url)

    def verify_transaction(self, reference, normalize="1", log_url=False):
        """

        :param log_url:
        :param reference:
        :param normalize:
        :return:
        """
        request_data = {
            "flw_ref": reference,
            "SECKEY": self.secret_key,
            "normalize": normalize
        }
        url = self.rave_url_map.get("payment_endpoint") + "verify"
        return self._exec_request("POST", url, request_data, log_url=log_url)

    def disburse(self, bank_code, account_number, currency, amount, log_url=False, ):
        """
        :param log_url:
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
        url = self.rave_url_map.get("disbursement_endpoint")
        return self._exec_request("POST", url, request_data, log_url=log_url)

    def tokenize_charge(self, token, log_url=False, **kwargs):
        """

        :param token:
        :param log_url:
        :param kwargs:
        :return:
        """
        kwargs["SECKEY"] = self.secret_key
        kwargs["token"] = token
        url = self.rave_url_map.get("payment_endpoint") + "tokenized/charge"
        return self._exec_request("POST", url, kwargs, log_url=log_url)

    def refund(self, reference_id, log_url=False, ):
        request_data = {
            "ref": reference_id,
            "seckey": self.secret_key,
        }
        url = self.rave_url_map.get("merchant_refund_endpoint")
        return self._exec_request("POST", url, request_data, log_url=log_url)

