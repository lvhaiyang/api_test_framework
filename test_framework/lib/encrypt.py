import hashlib
import hmac
import base64


def hmac_sha_base64(msg, mode, key):
    if mode == 'sha256':
        signature = hmac.new(key, msg.encode('utf-8'), digestmod=hashlib.sha256).digest()
        return base64.b64encode(signature)
    elif mode == 'sha1':
        signature = hmac.new(key, msg.encode('utf-8'), digestmod=hashlib.sha1).digest()
        return base64.b64encode(signature)




