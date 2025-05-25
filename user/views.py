# Error code: 1xxx
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class UserRegistrationView(APIView):
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def post(request):
        output = {"data": {}, "type": "success", "message": None}
        status_code = status.HTTP_201_CREATED
        user_serializer = UserRegistrationSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            output["message"] = "User Registration successfully."
        else:
            output["data"] = user_serializer.errors
            output["type"] = "error"
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(output, status=status_code)


class UserLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        output = {"data": {}, "type": "success", "message": None}
        status_code = status.HTTP_200_OK
        user_serializer = UserLoginSerializer(data=request.data)
        if user_serializer.is_valid():
            refresh = RefreshToken.for_user(user_serializer.instance)
            output.update(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        else:
            output.update({"message": "Invalid credentials", "type": "error"})
            status_code = status.HTTP_401_UNAUTHORIZED
        return Response(output, status=status_code)
