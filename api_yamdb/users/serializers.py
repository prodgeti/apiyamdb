from django.core.validators import RegexValidator, MaxLengthValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .utils import send_confirmation_email
from .mixins import UsernameAndEmailValidatorMixin

MAX_USERNAME_LENGTH = 150

User = get_user_model()


class UserSignupSerializer(
    UsernameAndEmailValidatorMixin,
    serializers.ModelSerializer
):
    """Сериализатор регистрации."""
    username = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Поле "username" должно содержать только буквы, '
                'цифры и символы: @/./+/-/_',
                code='invalid_username'
            ),
            MaxLengthValidator(MAX_USERNAME_LENGTH)
        ]
    )

    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        user, created = User.objects.get_or_create(
            username=username, email=email
        )
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        send_confirmation_email(email, confirmation_code)
        return user


class CustomTokenObtainSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')
        if not username:
            raise serializers.ValidationError(
                {'username': 'Имя пользователя обязательно.'})
        user = User.objects.filter(username=username).first()
        if not user:
            raise NotFound({'detail': 'Пользователь не найден.'})
        if not confirmation_code:
            raise serializers.ValidationError(
                {'confirmation_code': 'Код подтверждения обязателен.'})
        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError(
                {'confirmation_code': 'Недействительный код подтверждения.'})
        return attrs


class UserSerializer(
    UsernameAndEmailValidatorMixin,
    serializers.ModelSerializer
):
    """Сериализатор для работы с пользователями."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserMePatchSerializer(
    UsernameAndEmailValidatorMixin,
    serializers.ModelSerializer
):
    """Сериализатор для метода PATCH."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
