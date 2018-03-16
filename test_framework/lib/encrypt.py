import hashlib
import hmac
import base64


def sha256_base64(mag, key):
    signature = hmac.new(key, mag.encode('utf-8'), digestmod=hashlib.sha256).digest()
    return base64.b64encode(signature)


if __name__ == '__main__':
    password_key = b'KXLiUdAsO81ycDyEJAeETC$KklXdz3AC'
    # print(password_key)
    # print(type(password_key))
    # print(str(password_key, encoding='utf-8'))
    msg = '1qaz!QAZ'
    print(sha256_base64(msg, password_key))

