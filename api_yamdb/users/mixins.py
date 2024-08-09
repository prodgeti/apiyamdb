from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UsernameAndEmailValidatorMixin:
    """Миксин сериализатора юзера."""

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        if username == 'me':
            raise serializers.ValidationError(
                'Использование имени "me" запрещено.'
            )
        request = self.context.get('request')
        if request.method == 'POST':
            if not email:
                raise serializers.ValidationError(
                    'Поле "email" обязательно для заполнения.'
                )
        existing_user_by_username = User.objects.filter(
            username=username
        ).exists()
        existing_user_by_email = User.objects.filter(email=email).exists()
        if existing_user_by_username and existing_user_by_email:
            return attrs
        if existing_user_by_username:
            raise serializers.ValidationError(
                'Этот username уже используется.'
            )
        if existing_user_by_email:
            raise serializers.ValidationError(
                'Этот email уже используется.'
            )
        return attrs
