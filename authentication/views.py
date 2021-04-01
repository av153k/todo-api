from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJsonRenderer
from .serializers import (RegistrationSerializer,
                          LoginSerializer, UserSerializer)


class RegistrationApiView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJsonRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginApiView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJsonRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateApiView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJsonRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        
        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),
            'first_name': user_data.get('first_name', request.user.first_name),
            'last_name': user_data.get('last_name', request.user.last_name),
            'profile': {
                'phone': user_data.get('phone', request.user.profile.phone),
                'profile_picture': user_data.get('profile_picture', request.user.profile.profile_picture)
            }
        }
        print("Serializer data :---", serializer_data)

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
