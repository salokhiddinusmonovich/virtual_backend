from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from apps.accounts.serializers import (
    auth_serializers
)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = auth_serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = auth_serializers.RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request}, files=request.FILES)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



