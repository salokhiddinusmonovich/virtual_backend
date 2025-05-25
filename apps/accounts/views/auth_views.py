from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_spectacular.utils import extend_schema

from apps.accounts.serializers import (
    auth_serializers
)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = auth_serializers.LoginSerializer

    @extend_schema(
        request=auth_serializers.LoginSerializer,
        responses={200: auth_serializers.LoginSerializer},
        tags=['Auth'],
        description='Login user'
    )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
