from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework import permissions
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

        if user is not None:
            login(request, user)
            return Response({'message': 'Logged in successfully.'})
        else:
            return Response({'error': 'Invalid username or password.'}, status=401)


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

    def delete(self, request, *args, **kwargs):
        logout(request)
        return self.destroy(request, *args, **kwargs)


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
