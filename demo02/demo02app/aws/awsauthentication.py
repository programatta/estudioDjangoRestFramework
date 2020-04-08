from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions
from django.contrib.auth.models import User
import urllib.request
import json
import time
from django.conf import settings
from jose import jwk, jwt
from jose.utils import base64url_decode


class AWSTokenAuthentication(BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        # check structure
        if not self.__validateStructureJWT(token):
            raise exceptions.AuthenticationFailed('Invalid token')

        isOk, error = self.__validateSignatureJWS(token)
        if not isOk:
            print(error)
            return None, None

        userId, error = self.__verifyClaims(token)
        if userId is None:
            print(error)
            return None, None

        user = User()
        user.pk = userId
        user.is_active = True
        user.is_staff = False
        return user, None

    def __validateStructureJWT(self, token):
        # check header, payload and signature
        items = token.split('.')
        return len(items) == 3

    def __validateSignatureJWS(self, token):
        userPoolId = settings.AWS_CONFIG['USER_POOL_ID']
        region = settings.AWS_CONFIG['REGION']

        keysUrl = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userPoolId)
        with urllib.request.urlopen(keysUrl) as f:
            response = f.read()
        keys = json.loads(response.decode('utf-8'))['keys']

        headers = jwt.get_unverified_headers(token)
        kid = headers['kid']
        keyIndex = -1
        for i in range(len(keys)):
            if kid == keys[i]['kid']:
                keyIndex = i
                break
        if keyIndex == -1:
            return False, 'Public key not found in jwks.json'

        publicKey = jwk.construct(keys[keyIndex])
        payload, signature = str(token).rsplit('.', 1)
        decodedSignature = base64url_decode(signature.encode('utf-8'))
        if not publicKey.verify(payload.encode("utf8"), decodedSignature):
            return False, 'Signature verification failed'

        return True, None

    def __verifyClaims(self, token):
        clientId = settings.AWS_CONFIG['CLIENT_ID']

        claims = jwt.get_unverified_claims(token)
        if time.time() > claims['exp']:
            return None, 'Token is expired'

        audKey = 'aud' if claims['token_use'] == 'id' else 'client_id'
        if claims[audKey] != clientId:
            return False, 'Token was not issued for this audience'

        return claims['sub'], None
