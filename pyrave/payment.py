from pyrave.base import BaseRaveAPI
from pyrave.encryption import RaveEncryption
from pyrave.errors import MissingParamError


class Payment(BaseRaveAPI):
    def __init__(self):
        super(Payment, self).__init__()

    def pay(self, method="pay", using="card", preauthorised=False, **kwargs):
        """

        :param method:
        :param using:
        :param preauthorised:
        :param kwargs:
        :return:
        """
        rave_enc = RaveEncryption()
        endpoint = self.payment_endpoint + "charge"
        if method == "pay":
            if not kwargs.get("form.suggested_auth") and not kwargs.get("form.pin"):
                raise MissingParamError("You need to pass the PIN and SUGGESTED_AUTH parameters in the function call "
                                        "to make a payment")
        encrypted_data = rave_enc.encrypt(using, preauthorised, **kwargs)
        if not encrypted_data[0] == "201" or method == "get_pin":
            return encrypted_data
        request_data = encrypted_data[1]
        url = self._path(endpoint)
        return self._exec_request("POST", url, request_data)

    def validate_charge(self, key, reference, otp, method="card"):
        request_data = {
            "PBFPubKey": key,
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

    def capture_preauthorised_transaction(self, transaction_reference):
        """

        :param transaction_reference:
        :return:
        """
        endpoint = self.payment_endpoint + "capture"
        request_data = {
                "SECKEY": self.secret_key,
                "flwRef": transaction_reference,
        }
        url = self._path(endpoint)
        return self._exec_request("POST", url, request_data)

    def refund_or_void_transaction(self, action, reference_id):
        """

        :param action:
        :param reference_id:
        :return:
        """
        endpoint = self.payment_endpoint + "refundorvoid"
        request_data = {
                "ref": reference_id,
                "action": action,
                "SECKEY": self.secret_key
        }
        url = self._path(endpoint)
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