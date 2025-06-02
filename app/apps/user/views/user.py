from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.user import RegisterSerializer
from ..utils import set_jwt_cookies


class LogInAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(
            request=request,
            email=email,
            password=password
        )

        if user:
            response = Response(
                status=status.HTTP_200_OK
            )

            set_jwt_cookies(response=response, user=user)

            return response

        else:
            return Response(
                data={"message": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogOutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response(status=status.HTTP_200_OK)
        refresh_token = RefreshToken(request.COOKIES.get('refresh_token'))
        refresh_token.blacklist()
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response = Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

        set_jwt_cookies(response, user)

        return response

class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer = RegisterSerializer

    def get(self, request):
        return Response(data=self.serializer(request.user).data, status=status.HTTP_200_OK)
