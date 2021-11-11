from django.contrib.auth import login
from django.contrib.auth.models import User
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserProfile
from .serializers import RegisterSerializer, UserSerializer, UserProfileSerializer


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response("Registered Successfully with name {}".format(user.username))


# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


# Get User API
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


# Get User profile API
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.query_params.get('user'):
            User.objects.get(id=self.request.query_params.get('user'))
        return self.queryset.filter(id=self.request.query_params.get('user'))

    def update(self, request, **kwargs):
        user_obj = User.objects.get(id=kwargs.get('pk'))
        if request.data.get('username'):
            user_obj.username = request.data.get('username')
            user_obj.save()
            return Response(self.serializer_class(user_obj).data)
