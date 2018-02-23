import base64
from Crypto.Cipher import DES3
import hashlib
from pyrave.base import BaseRaveAPI


class RaveEncryption(BaseRaveAPI):
    """
    Base Encryption Class
    Encrypts User Details and returns pubkey, client and algo
    """
    def __init__(self):
        super(RaveEncryption, self).__init__()

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
        url = self.rave_url_map.get("test_encryption_url") if self.implementation == "test" else self.pyrave_encrypt(**kwargs)
        if using == "account":
            account_params.update(common_params)
            return self._exec_request("POST", url, data=account_params)
        card_params.update(common_params)
        return self._exec_request("POST", url, data=card_params, log_url=log_url)

    def pyrave_encrypt(self,  **kwargs):
        hashedseckey = hashlib.md5(self.secret_key.encode("utf-8")).hexdigest()
        hashedseckeylast12 = hashedseckey[-12:]
        seckeyadjusted = self.secret_key.replace('FLWSECK-', '')
        seckeyadjustedfirst12 = seckeyadjusted[:12]
        key = seckeyadjustedfirst12 + hashedseckeylast12
        blockSize = 8
        padDiff = blockSize - (len(kwargs) % blockSize)
        cipher = DES3.new(key, DES3.MODE_ECB)
        plainText = "{}{}".format(kwargs, "".join(chr(padDiff) * padDiff))
        encrypted = base64.b64encode(cipher.encrypt(plainText))
        return encrypted



