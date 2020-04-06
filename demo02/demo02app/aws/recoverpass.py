import boto3
# import botocore.exceptions
from demo02app.aws.utils.util import secretHash


class RecoverPasswordHelper:
    def __init__(self, conf):
        self._conf = conf

    def doRecoverPassword(self, email):
        boto3.setup_default_session(region_name=self._conf.REGION)
        client = boto3.client('cognito-idp')
        try:
            hashVal = secretHash(
                email+self._conf.CLIENT_ID,
                self._conf.CLIENT_SECRET
            )
            client.forgot_password(
                ClientId=self._conf.CLIENT_ID,
                SecretHash=hashVal,
                Username=email
            )
        except client.exceptions.UserNotFoundException:
            return {'status': 'error', 'error': 'Username doesnt exists'}
        except client.exceptions.InvalidParameterException:
            return {'status': 'error', 'error': 'User is not confirmed yet'}
        except client.exceptions.CodeMismatchException:
            return {'status': 'error', 'error': 'Invalid Verification code'}
        except client.exceptions.NotAuthorizedException:
            return {'status': 'error', 'error': 'User is already confirmed'}
        except Exception as e:
            return {'status': 'error', 'error': f'Uknown error {e.__str__()}'}

        return {
            'status': 'ok',
            'message': 'Please check your Registered email id for validation\
                code'
        }
