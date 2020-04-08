from rest_framework import exceptions
import boto3
import json
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode
from demo02app.aws.utils.util import secretHash


class RefreshTokensHelper:
    def __init__(self, conf):
        self._conf = conf

    def doRefreshTokens(self, refreshToken, idToken):
        boto3.setup_default_session(region_name=self._conf.REGION)

        error = self.__checkValidToken(idToken)
        if error is not None:
            return {'status': 'error', 'error': error}
        else:
            cognitoUUID, error = self.__checkIsIdToken(idToken)
            if error is not None:
                return {'status': 'error', 'error': error}
            else:
                resp, error = self._refreshAuth(refreshToken, cognitoUUID)
                if error is not None:
                    return {'status': 'error', 'error': error}
                elif resp.get("AuthenticationResult"):
                    return {
                        'status': 'ok',
                        'data': {
                            'id_token': resp["AuthenticationResult"]["IdToken"],
                            'access_token': resp["AuthenticationResult"]["AccessToken"],
                            'expires_in': resp["AuthenticationResult"]["ExpiresIn"],
                            'token_type': resp["AuthenticationResult"]["TokenType"]
                        }
                    }
                else:
                    return {
                        'status': 'error',
                        'error': 'Unexpected response from AWS',
                        'data': resp
                    }

    def __checkValidToken(self, token):
        # check structure
        if not self.__validateStructureJWT(token):
            raise exceptions.AuthenticationFailed('Invalid token')

        isOk, error = self.__validateSignatureJWS(token)
        if not isOk:
            print(error)
            return error
        else:
            return None

    def __validateStructureJWT(self, token):
        # check header, payload and signature
        items = token.split('.')
        return len(items) == 3

    def __validateSignatureJWS(self, token):
        userPoolId = self._conf.USER_POOL_ID
        region = self._conf.REGION

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

    def __checkIsIdToken(self, token):
        clientId = self._conf.CLIENT_ID

        claims = jwt.get_unverified_claims(token)

        if claims['token_use'] == 'id':
            if claims['aud'] != clientId:
                return None, 'Token was not issued for this audience'
            else:
                return claims['sub'], None
        else:
            return None, 'This token is not a Id Token'

    def _refreshAuth(self, refreshToken, cognitoUUID):
        client = boto3.client(
            'cognito-idp',
            aws_access_key_id=self._conf.ACCESSKEYID,
            aws_secret_access_key=self._conf.SECRETACCESSKEY
        )

        hashVal = secretHash(
            cognitoUUID+self._conf.CLIENT_ID,
            self._conf.CLIENT_SECRET
        )

        try:
            boto3.set_stream_logger('botocore', level='DEBUG')
            resp = client.admin_initiate_auth(
                UserPoolId=self._conf.USER_POOL_ID,
                ClientId=self._conf.CLIENT_ID,
                AuthFlow='REFRESH_TOKEN_AUTH',
                AuthParameters={
                    'REFRESH_TOKEN': refreshToken,
                    'SECRET_HASH': hashVal
                }
            )
        except client.exceptions.NotAuthorizedException as e:
            return None, e.__str__()
        except client.exceptions.UserNotConfirmedException:
            return None, 'User is not confirmed'
        except Exception as e:
            return None, e.__str__()
        return resp, None
