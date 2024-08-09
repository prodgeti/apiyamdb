from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserSignupViewSet,
    CustomTokenObtainPairView,
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
    UserAccountViewSet
)

router_v1 = DefaultRouter()
router_v1.register(
    r'v1/auth/signup', UserSignupViewSet, basename='user-signup'
)
router_v1.register(
    r'v1/users', UserListCreateAPIView, basename='user-list-create'
)
router_v1.register(
    r'v1/users', UserRetrieveUpdateDestroyAPIView, basename='user-detail'
)

urlpatterns = [
    path(
        'v1/auth/token/',
        CustomTokenObtainPairView.as_view(),
        name='token-obtain'
    ),
    path(
        'v1/users/me/',
        UserAccountViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update'}
        ),
        name='user-me-detail'),
    path('', include(router_v1.urls)),
]
