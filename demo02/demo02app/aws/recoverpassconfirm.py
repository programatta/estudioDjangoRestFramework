import boto3
import botocore.exceptions
from  demo02app.aws.utils.util import secretHash

class RecoverPasswordConfirmHelper:
    def __init__(self, conf):
        self._conf = conf
    
    def doRecoverPasswordConfirm(self, email, newpassword, code):
        boto3.setup_default_session(region_name=self._conf.REGION)
        client = boto3.client('cognito-idp')
        try:
            hashVal = secretHash(email+self._conf.CLIENT_ID, self._conf.CLIENT_SECRET)
            client.confirm_forgot_password(
                ClientId=self._conf.CLIENT_ID,
                SecretHash=hashVal,
                Username=email,
                ConfirmationCode=code,
                Password=newpassword
            )
        except client.exceptions.UserNotFoundException as e:
            return {'status':'error', 'error':'Username does not exists'}
        except client.exceptions.CodeMismatchException as e:
            return {'status':'error', 'error':'Invalid Verification code'}
        except client.exceptions.NotAuthorizedException as e:
            return {'status':'error', 'error':'User is already confirmed'}
        except Exception as e:
            return {'status':'error', 'error':f'Unknown error {e.__str__()}'}

        return {'status':'ok', 'message': 'Password has been changed successfully'}
