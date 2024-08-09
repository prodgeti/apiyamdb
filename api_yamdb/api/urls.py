from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CommentViewSet,
                       ReviewViewSet,
                       CategoryViewSet,
                       GenreViewSet,
                       TitleViewSet
                       )

router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register('categories', CategoryViewSet, basename='categorie')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
