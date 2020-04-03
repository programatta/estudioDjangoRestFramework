import boto3
import botocore.exceptions
from  demo02app.aws.utils.util import secretHash

class ResendCodeHelper:
    def __init__(self, conf):
        self._conf = conf
    
    def doResend(self, email):
        boto3.setup_default_session(region_name=self._conf.REGION)
        client = boto3.client('cognito-idp')
        status, error = self._checkUserConfirmed(client, email)
        if error != None:
            return {'status':'error', 'error': error}
        else:
            if status == 'UNCONFIRMED':
                try:
                    hashVal = secretHash(email+self._conf.CLIENT_ID, self._conf.CLIENT_SECRET)
                    client.resend_confirmation_code(
                        ClientId=self._conf.CLIENT_ID,
                        SecretHash=hashVal,
                        Username=email
                    )
                except client.exceptions.UserNotFoundException:
                    return {'status':'error', 'error': 'User does not exists'}
                except Exception as e:
                    return {'status':'error', 'error': f'Unknown error {e.__str__()}'}
            elif status == 'CONFIRMED':
                return {'status':'error', 'error': 'User is already confirmed'}
            else:
                return {'status':'error', 'error': 'User is in other state'}
        
        return {'status':'ok' ,'message':'Code sent again'}

    def _checkUserConfirmed(self, client, email):
        try:
            resp = client.admin_get_user(
                UserPoolId=self._conf.USER_POOL_ID,
                Username=email
            )
        except client.exceptions.UserNotFoundException:
            return None, 'User does not exists'
        except Exception as e:
            return None, f'Unknown error {e.__str__()}'
        
        if resp['UserStatus'] == 'CONFIRMED':
            return 'CONFIRMED', None
        elif resp['UserStatus'] == 'UNCONFIRMED':
            return 'UNCONFIRMED', None
        else:
            return 'OTHER', None