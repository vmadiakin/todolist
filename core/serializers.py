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

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        self.user = user
        return user

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

    def update(self, instance, validated_data):
        username = validated_data.get('username', instance.username)
        if User.objects.filter(username=username).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("Username already exists.")
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        user = self.context['request'].user

        if not user.check_password(old_password):
            raise serializers.ValidationError("Неправильный текущий пароль.")

        try:
            validate_password(new_password, user=user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(str(e))

        return data

    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')
        instance.set_password(new_password)
        instance.save()
        return instance
