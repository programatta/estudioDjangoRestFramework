from django.shortcuts import render
from django.http import JsonResponse
from .aws.awsview import AWSView
from .aws.signup import SignUpHelper
from .aws.confirmcode import ConfirmCodeHelper
from .aws.signin import SignInHelper
from .aws.resendcode import ResendCodeHelper
from .aws.recoverpass import RecoverPasswordHelper
from .aws.recoverpassconfirm import RecoverPasswordConfirmHelper

# Create your views here.

class SignUp(AWSView):
    def post(self, request):
        fields = self._checkParams(request,['name', 'email', 'password', 'birthdate', 'phoneNumber', 'address'])
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


class ConfirmCode(AWSView):
    def post(self, request):
        fields = self._checkParams(request, ['email', 'code']) 
        if fields != None:
            confirmCode = ConfirmCodeHelper(self._conf)
            response = confirmCode.doConfirmCode(
                email=fields['email'],
                code=fields['code']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status':'error','error':'Invalid params'})


class SignIn(AWSView):
    def post(self, request):
        fields = self._checkParams(request, ['email', 'password']) 
        if fields != None:
            signin = SignInHelper(self._conf)
            response = signin.doSignIn(
                email=fields['email'],
                password=fields['password']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status':'error','error':'Invalid params'})


class ResendCode(AWSView):
    def post(self, request):
        fields = self._checkParams(request, ['email']) 
        if fields != None:
            resend = ResendCodeHelper(self._conf)
            response = resend.doResend(
                email=fields['email']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status':'error','error':'Invalid params'})


class RecoverPassword(AWSView):
    def post(self, request):
        fields = self._checkParams(request, ['email']) 
        if fields != None:
            recover = RecoverPasswordHelper(self._conf)
            response = recover.doRecoverPassword(
                email=fields['email']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status':'error','error':'Invalid params'})


class RecoverPasswordConfirm(AWSView):
    def post(self, request):
        fields = self._checkParams(request, ['email','newpassword','code'])
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
