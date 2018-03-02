import base64
from Crypto.Cipher import DES3
from pyrave.base import BaseRaveAPI


class RaveEncryption(BaseRaveAPI):
    """
    Base Encryption Class
    Encrypts User Details and returns pubkey, client and algo
    """
    def __init__(self, implementation):
        super(RaveEncryption, self).__init__(implementation)

    def pyrave_encrypt(self, plain_text):
        blockSize = 8
        padDiff = blockSize - (len(plain_text) % blockSize)
        cipher = DES3.new(self.encryption_key, DES3.MODE_ECB)
        plain_text = "{}{}".format(plain_text, "".join(chr(padDiff) * padDiff))
        return base64.b64encode(cipher.encrypt(plain_text)).decode('utf-8')

    def integrity_checksum(self, **kwargs):
        plain_text = self.secret_key + ''.join(
                kwargs)
        return self.pyrave_encrypt(plain_text)

    def encrypt(self, using='card', preauthorised=False, log_url=False, **kwargs):
        """

        :param log_url:
        :param using: Card or Account
        :param preauthorised: Identifies if the transaction is preauthorised
        :param kwargs:
        :return:
        """
        common_params = {
            "seckey": self.secret_key,
            "pubkey": self.public_key,
            "form.PBFPubKey": self.public_key,
            "form.currency": kwargs.get('currency'),
            "form.country": kwargs.get('country'),
            "form.amount": kwargs.get('amount'),
            "form.email": kwargs.get('email'),
            "form.phonenumber": kwargs.get('phonenumber'),
            "form.firstname": kwargs.get('firstname'),
            "form.lastname": kwargs.get('lastname'),
            "form.IP": kwargs.get('IP'),
            "form.txRef": kwargs.get('txRef'),
            "form.device_fingerprint": kwargs.get('device_fingerprint', False)
        }
        card_params = {
            "form.cardno": kwargs.get('cardno'),
            "form.ccv": kwargs.get('ccv', True),
            "form.expirymonth": kwargs.get('expirymonth', True),
            "form.expiryyear": kwargs.get('expiryyear', True),
            "form.charge_type": kwargs.get('charge_type') if preauthorised else preauthorised

        }
        account_params = {
            "form.accountnumber": kwargs.get("accountnumber"),
            "form.accountbank": kwargs.get("accountbank"),
            "form.payment_type": kwargs.get("payment_type", "account")
        }
        url = self.rave_url_map.get("test_encryption_url") if self.implementation == "test" else self.rave_url_map.get("live_encryption_url")
        if using == "account":
            account_params.update(common_params)
            return self._exec_request("POST", url, data=account_params)
        card_params.update(common_params)
        if self.implementation == "test":
            return self._exec_request("POST", url, data=card_params, log_url=log_url)
        client = self.integrity_checksum(**card_params)
        return {
            'PBFPubKey': self.public_key,
            'client': client,
            'alg': '3DES-24'
        }


