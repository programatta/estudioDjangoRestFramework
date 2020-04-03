from django.views import View
from django.conf import settings
import json
from demo02app.aws.config import Config

class AWSView(View):
    def __init__(self):
        self._conf = Config(
            clientId=settings.AWS_CONFIG['CLIENT_ID'],
            secretClientId=settings.AWS_CONFIG['CLIENT_SECRET'],
            userPoolId=settings.AWS_CONFIG['USER_POOL_ID'],
            identityPoolId=settings.AWS_CONFIG['IDENTITY_POOL_ID'],
            region=settings.AWS_CONFIG['REGION'],
            accesskey=settings.AWS_CONFIG['ACCESSKEYID'],
            secretAccessKey=settings.AWS_CONFIG['SECRETACCESSKEY']
        )
    
    def _checkParams(self, request, expectedFields):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        for field in expectedFields:
            if not body.get(field):
                return None
        return body
    
    _conf = None