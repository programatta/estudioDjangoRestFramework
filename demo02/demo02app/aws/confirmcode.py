import boto3
import botocore.exceptions
from  demo02app.aws.utils.util import secretHash

class ConfirmCodeHelper:
    def __init__(self, conf):
        self._conf = conf
    
    def doConfirmCode(self, email, code):
        boto3.setup_default_session(region_name=self._conf.REGION)
        client = boto3.client('cognito-idp')
        try:
            hashVal = secretHash(email+self._conf.CLIENT_ID, self._conf.CLIENT_SECRET)
            client.confirm_sign_up(
                ClientId=self._conf.CLIENT_ID,
                SecretHash=hashVal,
                Username=email,
                ConfirmationCode=code,
                ForceAliasCreation=False,
            )
        except client.exceptions.UserNotFoundException:
            return {'status':'error', 'error':'User does not exists'}
            #return event
        except client.exceptions.CodeMismatchException:
            return {'status':'error', 'error':'Invalid Verification code'}
        except client.exceptions.NotAuthorizedException:
            return {'status':'error', 'error':'User is already confirmed'}
        except Exception as e:
            return {'status':'error', 'error': f'Unknown error {e.__str__()}'}
        
        return {'status':'ok','message':'Code verificated!'}


    _conf = None