from pyrave.base import BaseRaveAPI


class Transaction(BaseRaveAPI):
    """
    Transaction Classs.
    Handles Transaction Verification and requery.
    Also handles recurrent transaction.
    """
    def __init__(self):
        super(Transaction, self).__init__()

    def verify_transaction(self, normalize="1", flw_ref=None, tx_ref=None, log_url=False):
        """

        :param flw_ref:
        :param log_url:
        :param normalize:
        :param tx_ref:
        :return:
        """
        request_data = {
            "SECKEY": self.secret_key,
            "normalize": normalize
        }
        if tx_ref:
            request_data["tx_ref"] = tx_ref
        if flw_ref:
            request_data["flw_ref"] = flw_ref
        url = self.rave_url_map.get("payment_endpoint") + "verify"
        return self._exec_request("POST", url, request_data, log_url=log_url)

    def verify_transaction_with_xrequery(self, log_url=False, **kwargs):
        """
        :param kwargs:
        :param log_url:
        :return:
        """
        endpoint = self.rave_url_map.get("self.payment_endpoint") + "xrequery"
        url = self._path(endpoint)
        return self._exec_request("POST", url, kwargs, log_url=log_url)

    def get_reccurent_transactions(self, log_url=False):
        """

        :return:
        """
        request_data = {
            "SECKEY": self.secret_key
        }
        url = self.rave_url_map.get("recurring_transaction_endpoint") + "list"
        return self._exec_request("GET", url, request_data, log_url=log_url, params=True)

    def get_reccurrent_transaction(self, transaction_id, log_url=True):
        """

        :param transaction_id:
        :param log_url:
        :return:
        """
        request_data = {
            "SECKEY": self.secret_key,
            "txId": transaction_id
        }
        url = self.rave_url_map.get("recurring_transaction_endpoint") + "list"
        return self._exec_request("GET", url, request_data, log_url=log_url, params=True, )

    def stop_recurrent_transaction(self, transaction_data_id, log_url=False):
        """

        :param transaction_data_id:
        :param log_url:
        :return:
        """
        request_data = {
            "SECKEY": self.secret_key,
            "txId": transaction_data_id
        }
        url = self.rave_url_map.get("recurring_transaction_endpoint") + "stop"

        return self._exec_request("GET", url, request_data, log_url=log_url)




