from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from .aws.awsview import AWSView
from .aws.signup import SignUpHelper
from .aws.confirmcode import ConfirmCodeHelper
from .aws.signin import SignInHelper
from .aws.resendcode import ResendCodeHelper
from .aws.recoverpass import RecoverPasswordHelper
from .aws.recoverpassconfirm import RecoverPasswordConfirmHelper
from .aws.refreshtokens import RefreshTokensHelper
from .aws.awsauthentication import AWSTokenAuthentication
from .serializers import TransactionSerializer
from .models import Transaction

# Create your views here.


class SignUp(AWSView):
    def post(self, request):
        fields = self._checkParams(
            request,
            [
                'name', 'email', 'password',
                'birthdate', 'phoneNumber', 'address'
            ]
        )
        if fields is not None:
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
            return JsonResponse({'status': 'error', 'error': 'Invalid params'})


class ConfirmCode(AWSView):
    def post(self, request):
        fields = self._checkParams(request, ['email', 'code'])
        if fields is not None:
            confirmCode = ConfirmCodeHelper(self._conf)
            response = confirmCode.doConfirmCode(
                email=fields['email'],
                code=fields['code']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status': 'error', 'error': 'Invalid params'})


class SignIn(AWSView):
    def post(self, request):
        fields = self._checkParams(request, ['email', 'password'])
        if fields is not None:
            signin = SignInHelper(self._conf)
            response = signin.doSignIn(
                email=fields['email'],
                password=fields['password']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status': 'error', 'error': 'Invalid params'})


class ResendCode(AWSView):
    def post(self, request):
        fields = self._checkParams(request, ['email'])
        if fields is not None:
            resend = ResendCodeHelper(self._conf)
            response = resend.doResend(
                email=fields['email']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status': 'error', 'error': 'Invalid params'})


class RecoverPassword(AWSView):
    def post(self, request):
        fields = self._checkParams(request, ['email'])
        if fields is not None:
            recover = RecoverPasswordHelper(self._conf)
            response = recover.doRecoverPassword(
                email=fields['email']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status': 'error', 'error': 'Invalid params'})


class RecoverPasswordConfirm(AWSView):
    def post(self, request):
        fields = self._checkParams(request, ['email', 'newpassword', 'code'])
        if fields is not None:
            recoverConfirm = RecoverPasswordConfirmHelper(self._conf)
            response = recoverConfirm.doRecoverPasswordConfirm(
                email=fields['email'],
                newpassword=fields['newpassword'],
                code=fields['code'],
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status': 'error', 'error': 'Invalid params'})


class RefreshTokens(AWSView):
    def post(self, request):
        fields = self._checkParams(request, ['refreshToken', 'idToken'])
        if fields is not None:
            refreshTokens = RefreshTokensHelper(self._conf)
            response = refreshTokens.doRefreshTokens(
                refreshToken=fields['refreshToken'],
                idToken=fields['idToken']
            )
            return JsonResponse(response)
        else:
            return JsonResponse({'status': 'error', 'error': 'Invalid params'})

# API protegida por token.


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para transacciones.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    # permission_classes = [IsOwner, permissions.IsAuthenticated]
    authentication_classes = [AWSTokenAuthentication]

    def get_queryset(self):
        return Transaction.objects.filter(ownerId=self.request.user.id)

    def put(self, request, pk):
        return Response(request)
