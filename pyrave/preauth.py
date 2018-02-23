from pyrave.base import BaseRaveAPI


class Preauth(BaseRaveAPI):
    """
    Preauthorization Class

    """
    def __init__(self):
        super(Preauth, self).__init__()

    def preauthorise_card(self, client, algo):
        """

        :param client:
        :param algo:
        :return:
        """
        endpoint = self.payment_endpoint + "charge"
        request_data = {
                "PBFPubKey": self.public_key,
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
        request_data = {
                "ref": reference_id,
                "seckey": self.secret_key
        }
        url = self.merchant_refund_endpoint
        return self._exec_request("POST", url, request_data)


