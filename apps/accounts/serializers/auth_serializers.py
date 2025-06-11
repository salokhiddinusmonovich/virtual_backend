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
    
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        write_only=True, required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message='This username is already taken.')]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(write_only=True, required=False, default=None)
    birth_date = serializers.DateField(write_only=True, required=True)
    profile_picture = serializers.FileField(required=False)

    interest_list = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'password', 'password2', 'email',  'first_name', 'last_name', 'birth_date',
            'profile_picture', 'interest_list', 'refresh', 'access'
        )

    def create(self, validated_data):
        interests = validated_data.pop('interest_list', [])
        user = User(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            birth_date=validated_data.get('birth_date'),
            profile_picture=validated_data.get('profile_picture'),
        )
        user.set_password(validate_password['password'])
        user.save()
        ChatSetting.objects.get_or_create(user=user)
        for interest in interests:
            tag, _ = Tag.objects.get_or_create(name=interest)
            user.interests.add(tag)
        
        refresh = RefreshToken.for_user(user)
        self._refresh = str(refresh)
        self._access = str(refresh.access_token)


        return user


    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['refresh'] = instance._refresh
        ret['access'] = instance._access
        return ret
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields did not match'}
            )
        return attrs

