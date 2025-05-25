from random import sample
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import load_strategy, load_backend


from apps.chat.models import ChatSetting
from apps.content.models import Tag
from apps.accounts.models import User




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = PasswordField(write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def validate(self, attrs):
        request = self.context.get('request')
        user = authenticate(request, **attrs)
        if not user:
            raise AuthenticationFailed(detail='Invalid username or password')
        
        if not user.is_active:
            raise AuthenticationFailed(detail='User account is disabled')
        
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        update_last_login(None, user)
        return data
    
    @classmethod
    def get_token(cls, user) -> RefreshToken:
        return RefreshToken.for_user(user)
    
