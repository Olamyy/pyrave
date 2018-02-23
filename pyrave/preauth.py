from pyrave.base import BaseRaveAPI


class Preauth(BaseRaveAPI):
    """
    Preauthorization Class

    """
    def __init__(self):
        super(Preauth, self).__init__()

    def preauthorise_card(self, client, algo, log_url=False):
        """

        :param log_url:
        :param client:
        :param algo:
        :return:
        """
        request_data = {
                "PBFPubKey": self.public_key,
                "client": client,
                "alg": algo
        }
        url = self.rave_url_map.get("payment_endpoint") + "charge"
        return self._exec_request("POST", url, request_data, log_url=log_url)

    def capture_preauthorised_transaction(self, transaction_reference, log_url=False):
        """

        :param log_url:
        :param transaction_reference:
        :return:
        """
        request_data = {
                "SECKEY": self.secret_key,
                "flwRef": transaction_reference,
        }
        url = self.rave_url_map.get("payment_endpoint") + "capture"
        return self._exec_request("POST", url, request_data, log_url=log_url)

    def refund_or_void_transaction(self, action, reference_id, log_url=False):
        """

        :param log_url:
        :param action:
        :param reference_id:
        :return:
        """
        request_data = {
                "ref": reference_id,
                "action": action,
                "SECKEY": self.secret_key
        }
        url = self.rave_url_map.get("payment_endpoint") + "refundorvoid"
        return self._exec_request("POST", url, request_data, log_url=log_url)

    def refund(self, reference_id, log_url=False):
        request_data = {
                "ref": reference_id,
                "seckey": self.secret_key
        }
        url = self.rave_url_map.get("merchant_refund_endpoint")
        return self._exec_request("POST", url, request_data, log_url=log_url)



