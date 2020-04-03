from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.conf import settings 
#from rest_framework.views import APIView
#from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import json
from .aws.config import Config
from .aws.signup import SignUpHelper
from .aws.confirmcode import ConfirmCodeHelper
from .aws.signin import SignInHelper
from .aws.resendcode import ResendCodeHelper
from .aws.recoverpass import RecoverPasswordHelper
from .aws.recoverpassconfirm import RecoverPasswordConfirmHelper

# Create your views here.

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class SignUp(View):
    #authentication_classes = (CsrfExemptSessionAuthentication)
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

    #@csrf_exempt
    def post(self, request):
        fields = self._checkParams( request ) 
        if fields != None:
            signup = SignUpHelper(self._conf)
            response = signup.doSignUp(
                name=fields['name'], 
                email=fields['email'],
                password=fields['password'], 
                birthdate=fields['birthdate'], 
                phoneNumber=fields['phoneNumber'],
                address=fields['address']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status':'error','error':'Invalid params'})

    def _checkParams(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        for field in ['name', 'email', 'password', 'birthdate', 'phoneNumber', 'address']:
            if not body.get(field):
                return None
        return body
    
    _conf = None


class ConfirmCode(View):
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

    def post(self, request):
        fields = self._checkParams( request ) 
        if fields != None:
            confirmCode = ConfirmCodeHelper(self._conf)
            response = confirmCode.doConfirmCode(
                email=fields['email'],
                code=fields['code']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status':'error','error':'Invalid params'})

    def _checkParams(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        for field in ['email', 'code']:
            if not body.get(field):
                return None
        return body
    
    _conf = None


class SignIn(View):
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

    def post(self, request):
        fields = self._checkParams( request ) 
        if fields != None:
            signin = SignInHelper(self._conf)
            response = signin.doSignIn(
                email=fields['email'],
                password=fields['password']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status':'error','error':'Invalid params'})

    def _checkParams(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        for field in ['email', 'password']:
            if not body.get(field):
                return None
        return body
    
    _conf = None


class ResendCode(View):
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

    def post(self, request):
        fields = self._checkParams( request ) 
        if fields != None:
            resend = ResendCodeHelper(self._conf)
            response = resend.doResend(
                email=fields['email']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status':'error','error':'Invalid params'})

    def _checkParams(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        for field in ['email']:
            if not body.get(field):
                return None
        return body
    
    _conf = None


class RecoverPassword(View):
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

    def post(self, request):
        fields = self._checkParams( request ) 
        if fields != None:
            recover = RecoverPasswordHelper(self._conf)
            response = recover.doRecoverPassword(
                email=fields['email']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status':'error','error':'Invalid params'})

    def _checkParams(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        for field in ['email']:
            if not body.get(field):
                return None
        return body
    
    _conf = None


class RecoverPasswordConfirm(View):
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

    def post(self, request):
        fields = self._checkParams( request ) 
        if fields != None:
            recoverConfirm = RecoverPasswordConfirmHelper(self._conf)
            response = recoverConfirm.doRecoverPasswordConfirm(
                email=fields['email'],
                newpassword=fields['newpassword'], 
                code=fields['code'],
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status':'error','error':'Invalid params'})

    def _checkParams(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        for field in ['email','newpassword','code']:
            if not body.get(field):
                return None
        return body
    
    _conf = None