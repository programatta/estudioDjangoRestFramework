import boto3
import botocore.exceptions
import json
from  demo02app.aws.utils.util import secretHash

class SignUpHelper:
    def __init__(self, conf):
        self._conf = conf

    def doSignUp(self, name, email, password, birthdate, phoneNumber, address):
        username = email

        boto3.setup_default_session(region_name='us-west-2')
        client = boto3.client('cognito-idp')
        try:
            hashVal = secretHash(username+self._conf.CLIENT_ID, self._conf.CLIENT_SECRET)
            resp = client.sign_up(
                ClientId=self._conf.CLIENT_ID,
                SecretHash=hashVal,
                Username=username,
                Password=password, 
                UserAttributes=[
                    {
                        'Name': 'name',
                        'Value': name
                    },
                    {
                        'Name': 'email',
                        'Value': email
                    },
                    {
                        'Name': 'phone_number',
                        'Value': phoneNumber
                    },
                    {
                        'Name': 'family_name',
                        'Value': 'Latter Pay'
                    },
                    {
                        'Name': 'birthdate',
                        'Value': birthdate
                    },
                    {
                        'Name': 'address',
                        'Value': address
                    }
                ],
                ValidationData=[
                    {
                        'Name': 'email',
                        'Value': email
                    },
                    {
                        'Name': 'custom:username',
                        'Value': username
                    }
                ]
            )
            print(resp)
        except client.exceptions.UsernameExistsException as e:
            return {
                'status': 'error', 
                'error': 'This user already exists', 
                'data': None
            }
        except client.exceptions.InvalidPasswordException as e:
            return {
                'status': 'error',
                'error': 'Password should have Caps, Special chars, Numbers', 
                'data': None
            }
        except client.exceptions.UserLambdaValidationException as e:
            return {
                'status':'error', 
                'error': 'Email already exists',
                'data': None
            }
        except Exception as e:
            return {
                'status':'error', 
                'error': str(e), 
                'data': None
            }
    
        return {
            'status': 'ok', 
            'message': 'Please check Email for validation code', 
            'data': None
        }


    _conf = None