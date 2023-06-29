from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password_repeat', 'role', 'birthdate']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password_repeat = attrs.pop('password_repeat', None)

        # Проверка совпадения паролей
        if password != password_repeat:
            raise serializers.ValidationError("Пароли не совпадают.")

        # Проверка надежности пароля с помощью встроенной проверки Django
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(e.args[0])

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')

        # Создание пользователя с хешированным паролем
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
