import hmac
import hashlib
import base64


def secretHash(message, secret):
    dig = hmac.new(
        str(secret).encode('utf-8'),
        msg=str(message).encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    d2 = base64.b64encode(dig).decode()
    return d2
