import boto3


class RemoveUserHelper:
    def __init__(self, conf):
        self._conf = conf

    def doRemoveUser(self, accessToken):
        boto3.setup_default_session(region_name=self._conf.REGION)

        resp, error = self.__removeUser(accessToken)
        if error is not None:
            return {'status': 'error', 'error': error}
        else:
            return {'status': 'ok'}

    def __removeUser(self, accessToken):
        client = boto3.client(
            'cognito-idp',
            aws_access_key_id=self._conf.ACCESSKEYID,
            aws_secret_access_key=self._conf.SECRETACCESSKEY
        )

        try:
            boto3.set_stream_logger('botocore', level='DEBUG')
            resp = client.delete_user(
                AccessToken=accessToken
            )
        except client.exceptions.NotAuthorizedException as e:
            return None, e.__str__()
        except client.exceptions.UserNotConfirmedException:
            return None, 'User is not confirmed'
        except Exception as e:
            return None, e.__str__()
        return resp, None
