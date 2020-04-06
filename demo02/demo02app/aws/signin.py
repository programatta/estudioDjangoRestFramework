import boto3
# import botocore.exceptions
# import json
from demo02app.aws.utils.util import secretHash


class SignInHelper:
    def __init__(self, conf):
        self._conf = conf

    def doSignIn(self, email, password):
        boto3.setup_default_session(region_name=self._conf.REGION)

        resp, error = self._initiateAuth(email, password)
        if error is not None:
            return {'status': 'error', 'error': error}
        elif resp.get("AuthenticationResult"):
            tokenId = resp["AuthenticationResult"]["IdToken"]
            identityId, error = self._getIdentity(tokenId)
            if error is not None:
                return {'status': 'error', 'error': error}
            else:
                credentials, error = self._getCredentialsForIdentity(identityId, tokenId)
                if error is not None:
                    return {'status': 'error', 'error': error}
                else:
                    return {
                        'status': 'ok',
                        'data': {
                            'id_token': resp["AuthenticationResult"]["IdToken"],
                            'refresh_token': resp["AuthenticationResult"]["RefreshToken"],
                            'access_token': resp["AuthenticationResult"]["AccessToken"],
                            'expires_in': resp["AuthenticationResult"]["ExpiresIn"],
                            'token_type': resp["AuthenticationResult"]["TokenType"],
                            'identity_id': identityId,
                            'credentials': credentials
                        }
                    }
        else:
            return {
                'status': 'error',
                'error': 'Unexpected response from AWS',
                'data': resp
            }

    def _initiateAuth(self, email, password):
        client = boto3.client('cognito-idp',
            aws_access_key_id=self._conf.ACCESSKEYID,
            aws_secret_access_key=self._conf.SECRETACCESSKEY
        )
        hashVal = secretHash(
            email+self._conf.CLIENT_ID,
            self._conf.CLIENT_SECRET
        )
        try:
            # boto3.set_stream_logger('botocore', level='DEBUG')
            resp = client.admin_initiate_auth(
                UserPoolId=self._conf.USER_POOL_ID,
                ClientId=self._conf.CLIENT_ID,
                AuthFlow='ADMIN_USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'SECRET_HASH': hashVal,
                    'PASSWORD': password,
                },
                ClientMetadata={
                    'username': email,
                    'password': password,
                }
            )
        except client.exceptions.NotAuthorizedException:
            return None, 'The email or password is incorrect'
        except client.exceptions.UserNotConfirmedException:
            return None, 'User is not confirmed'
        except Exception as e:
            return None, e.__str__()
        return resp, None

    def _getIdentity(self, tokenId):
        client = boto3.client('cognito-identity')
        try:
            loginKey = f'cognito-idp.us-west-2.amazonaws.com/{self._conf.USER_POOL_ID}'
            logins = {}
            logins[loginKey] = tokenId
            resp = client.get_id(
                IdentityPoolId=self._conf.IDENTITY_POOL_ID,
                Logins=logins
            )
        except Exception as e:
            return None, e.__str__()

        return resp['IdentityId'], None

    def _getCredentialsForIdentity(self, identityId, tokenId):
        client = boto3.client('cognito-identity')
        try:
            loginKey = f'cognito-idp.us-west-2.amazonaws.com/{self._conf.USER_POOL_ID}'
            logins = {}
            logins[loginKey] = tokenId
            resp = client.get_credentials_for_identity(
                IdentityId=identityId,
                Logins=logins
            )
        except Exception as e:
            return None, e.__str__()

        return {
            'access_key_id': resp['Credentials']['AccessKeyId'],
            'secret_key': resp['Credentials']['SecretKey'],
            'session_token': resp['Credentials']['SessionToken'],
            'expiration': resp['Credentials']['Expiration']
        }, None

    _conf = None
