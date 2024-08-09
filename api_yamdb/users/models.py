from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        max_length=20,
        choices=CHOICES,
        default='user',
        verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name='Код подтверждения'
    )

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'

    def clean(self):
        super().clean()
        if self.username == 'me':
            raise ValidationError(
                {'username': 'Использование имени "me" в качестве username '
                 'запрещено.'}
            )
        if CustomUser.objects.exclude(
            id=self.id
        ).filter(username=self.username).exists():
            raise ValidationError(
                {'username': 'Этот username уже используется.'}
            )
        if self.email:
            if CustomUser.objects.exclude(
                id=self.id
            ).filter(email=self.email).exists():
                raise ValidationError(
                    {'email': 'Этот email уже используется.'}
                )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username
