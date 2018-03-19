import base64
from Crypto.Cipher import DES3
from pyrave.base import BaseRaveAPI


class RaveEncryption(BaseRaveAPI):
    """
    Base Encryption Class
    Encrypts User Details and returns pubkey, client and algo
    """
    def __init__(self):
        super(RaveEncryption, self).__init__()

    def pyrave_encrypt(self, plain_text):
        blockSize = 8
        padDiff = blockSize - (len(plain_text) % blockSize)
        cipher = DES3.new(self.encryption_key, DES3.MODE_ECB)
        plain_text = "{}{}".format(plain_text, "".join(chr(padDiff) * padDiff))
        return base64.b64encode(cipher.encrypt(plain_text)).decode('utf-8')

    def integrity_checksum(self, **kwargs):
        values = []
        for key in sorted(kwargs.keys()):
            values.append(kwargs[key])
        text = self.secret_key + ''.join(
                kwargs)
        return self.pyrave_encrypt(text)

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
            "PBFPubKey": self.public_key,
            "currency": kwargs.get('currency'),
            "country": kwargs.get('country'),
            "amount": kwargs.get('amount'),
            "email": kwargs.get('email'),
            "phonenumber": kwargs.get('phonenumber'),
            "firstname": kwargs.get('firstname'),
            "lastname": kwargs.get('lastname'),
            "IP": kwargs.get('IP'),
            "txRef": kwargs.get('txRef'),
            "device_fingerprint": kwargs.get('device_fingerprint', False)
        }
        card_params = {
            "cardno": kwargs.get('cardno'),
            "cvv": kwargs.get('cvv'),
            "expirymonth": kwargs.get('expirymonth', True),
            "expiryyear": kwargs.get('expiryyear', True),
        }
        if preauthorised:
            card_params["charge_type"] = preauthorised

        account_params = {
            "accountnumber": kwargs.get("accountnumber"),
            "accountbank": kwargs.get("accountbank"),
            "payment_type": kwargs.get("payment_type", "account")
        }
        if self.implementation == "live":
            if using == "acount":
                account_params.update(common_params)
                client = self.pyrave_encrypt(**account_params)
                return {
                    'PBFPubKey': self.public_key,
                    'client': client,
                    'alg': '3DES-24'
                }
            card_params.update(common_params)
            import json
            ca = json.dumps(card_params)
            client = self.pyrave_encrypt(ca)
            print(client)
            return {
                'PBFPubKey': self.public_key,
                'client': client,
                'alg': '3DES-24'
            }
        url = self.rave_url_map.get("test_encryption_url")
        if using == "account":
            account_params.update(common_params)
            return self._exec_request("POST", url, data=account_params, log_url=log_url)
        card_params.update(common_params)
        return self._exec_request("POST", url, data=card_params, log_url=log_url)



