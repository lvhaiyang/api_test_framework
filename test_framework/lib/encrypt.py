import hashlib
import hmac
import base64


def sha256_base64(mag, key):
    signature = hmac.new(key, mag.encode('utf-8'), digestmod=hashlib.sha256).digest()
    return base64.b64encode(signature)




