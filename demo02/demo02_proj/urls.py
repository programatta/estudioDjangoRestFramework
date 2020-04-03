"""demo02_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from demo02app import views
from django.views.decorators.csrf import csrf_exempt    # no me mola mucho.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/signup/', csrf_exempt(views.SignUp.as_view())),
    path('auth/confirmcode/', csrf_exempt(views.ConfirmCode.as_view())),
    path('auth/signin/', csrf_exempt(views.SignIn.as_view())),
    path('auth/resendcode/', csrf_exempt(views.ResendCode.as_view())),
    path('auth/recoverpass/', csrf_exempt(views.RecoverPassword.as_view())),
    path('auth/recoverpassconfirm/', csrf_exempt(views.RecoverPasswordConfirm.as_view()))
]
