from pyrave.base import BaseRaveAPI


class Transaction(BaseRaveAPI):
    """
    Transaction Classs.
    Handles Transaction Verification and requery.
    Also handles recurrent transaction.
    """
    def __init__(self):
        super(Transaction, self).__init__()

    def verify_transaction(self, reference,  normalize="1", tx_ref=None):
        """

        :param reference:
        :param normalize:
        :param tx_ref:
        :return:
        """
        endpoint = self.payment_endpoint + "verify"
        request_data = {
            "SECKEY": self.secret_key,
            "normalize": normalize
        }
        if tx_ref:
            request_data["tx_ref"] = tx_ref
        if reference:
            request_data["reference"] = reference
        url = self._path(endpoint)
        return self._exec_request("POST", url, request_data)

    def verify_transaction_with_xrequery(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        endpoint = self.payment_endpoint + "xrequery"
        url = self._path(endpoint)
        return self._exec_request("POST", url, kwargs)

    def get_reccurent_transactions(self):
        """

        :return:
        """
        endpoint = self.recurring_transaction_endpoint + "list"
        request_data = {
            "SECKEY": self.secret_key
        }
        url = self._path(endpoint)
        return self._exec_request("GET", url, request_data)

    def get_reccurrent_transaction(self, transaction_id):
        """

        :param transaction_id:
        :return:
        """
        endpoint = self.payment_endpoint + "list"
        request_data = {
            "SECKEY": self.secret_key,
            "txId": transaction_id
        }
        url = self._path(endpoint)
        return self._exec_request("GET", url, request_data)

    def stop_recurrent_transaction(self, transaction_data_id):
        """

        :param transaction_data_id:
        :return:
        """
        endpoint = self.payment_endpoint + "stop"
        request_data = {
            "SECKEY": self.secret_key,
            "txId": transaction_data_id
        }
        url = self._path(endpoint)
        return self._exec_request("GET", url, request_data)
