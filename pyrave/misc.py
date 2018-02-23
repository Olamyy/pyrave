from pyrave.base import BaseRaveAPI


class Misc(BaseRaveAPI):
    """
    Base Miscellaneous class
    """
    def __init__(self):
        super(Misc, self).__init__()

    def get_banks(self):
        endpoint = self.payment_endpoint + "flwpbf-banks.js?json=1"
        """

        :return:
        """
        url = self._path(endpoint)
        return self._exec_request('GET', url)

    def get_fee(self, amount, currency, ptype, card6=None):
        """

        :param amount: This is the amount of the product or service to charged from the customer
        :param currency: This is the specified currency to charge the card in.
        :param ptype: This is an optional parameter to be used when the payment type is account payment.
        A value of 2 is to be passed to the endpoint.
        :param card6: This can be used only when the user has entered first 6digits of their card number,
                    it also helps determine international fees on the transaction
                    if the card being used is an international card
        :return:
        """
        endpoint = self.payment_endpoint + "fee"
        request_data = {
            "amount": amount,
            "currency": currency,
            "ptype": ptype,
            "PBFPubKey": self.public_key,
            "card6": card6,
        }
        url = self._path(endpoint)
        return self._exec_request('POST', url, request_data)

    def get_exchange_rates(self, origin_currency, destination_currency, amount=None):
        """

        :param amount:
        :param origin_currency:
        :param destination_currency:
        :return:
        """
        endpoint = self.payment_endpoint + "forex"
        request_data = {
            "origin_currency": origin_currency,
            "destination_currency": destination_currency,
            "SECKEY": self.secret_key
        }
        if amount:
            request_data["amount"] = amount
        url = self._path(endpoint)
        return self._exec_request('POST', url, request_data)

