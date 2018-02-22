from pyrave.base import BaseRaveAPI


class Preauth(BaseRaveAPI):
    def __init__(self):
        super(Payment, self).__init__()

    def preauthorise_card(self, client, algo):
        """

        :param client:
        :param algo:
        :return:
        """
        endpoint = self.payment_endpoint + "charge"
        request_data = {
                "PBFPubKey": self.secret_key,
                "client": client,
                "alg": algo
        }
        url = self._path(endpoint)
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

    def refund(self, reference_id):
        endpoint = self.refund_transaction_endpoint + "refund"
        request_data = {
                "ref": reference_id,
                "SECKEY": self.secret_key
        }
        url = self._path(endpoint)
        return self._exec_request("POST", url, request_data)

