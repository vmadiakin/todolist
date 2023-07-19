from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from .models import User
from .serializers import UserRegistrationSerializer, UserSerializer, ChangePasswordSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    model = User
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        login(
            self.request,
            user=serializer.user,
            backend="django.contrib.auth.backends.ModelBackend",
        )


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'error': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)

        login_data = {
            'username': username,
            'password': password
        }

        return Response(login_data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        response["X-CSRFToken"] = get_token(self.request)
        return response

    @method_decorator(login_required)
    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({'message': 'Logged out successfully.'})


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        if not user.check_password(old_password):
            return Response({'old_password': 'Неправильный текущий пароль.'}, status=400)

        if old_password == new_password:
            return Response({'new_password': 'Новый пароль должен отличаться от текущего.'}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Пароль успешно изменен.'})
