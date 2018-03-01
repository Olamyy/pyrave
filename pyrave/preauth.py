from pyrave.base import BaseRaveAPI
from pyrave.encryption import RaveEncryption


class Preauth(BaseRaveAPI):
    """
    Preauthorization Class

    """

    def __init__(self):
        super(Preauth, self).__init__()
        self.rave_enc = RaveEncryption()

    def preauthorise_card(self, log_url=False, **kwargs):
        """

        :param log_url:
        :param client:
        :param algo:
        :return:
        """
        encrypted_data = self.rave_enc.encrypt(preauthorised=True, **kwargs)
        if not encrypted_data:
            return encrypted_data
        request_data = {
            "PBFPubKey": self.secret_key,
            "client": encrypted_data[1],
            "algo": encrypted_data[2]
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
