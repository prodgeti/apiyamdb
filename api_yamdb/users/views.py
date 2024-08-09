from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed

from .serializers import (
    UserSignupSerializer,
    CustomTokenObtainSerializer,
    UserSerializer,
    UserMePatchSerializer
)
from api.permissions import IsAdmin, IsSuperuser

User = get_user_model()


class UserSignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Класс представления создания пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Класс представления получения JWT-токена."""
    serializer_class = CustomTokenObtainSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.get(username=data['username'])
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        return Response(
            {'token': str(access_token)},
            status=status.HTTP_200_OK
        )


class UserListCreateAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """Класс представления создания пользователя и списка пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin | IsSuperuser, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )


class UserRetrieveUpdateDestroyAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Класс представления управления пользователем."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    permission_classes = (IsAdmin | IsSuperuser, )
    http_method_names = ('get', 'patch', 'delete', )


class UserAccountViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """Класс представления своей учётной записи."""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )
    http_method_names = ('get', 'patch', )

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UserMePatchSerializer
        return UserSerializer

    def get_object(self):
        user = self.request.user
        return user

    def partial_update(self, request, *args, **kwargs):
        if 'role' in request.data:
            raise MethodNotAllowed(
                'PATCH',
                detail='Невозможно изменить поле "role".'
            )
        return super().update(request, *args, **kwargs, partial=True)
