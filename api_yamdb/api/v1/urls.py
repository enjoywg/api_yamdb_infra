from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    GetTokenView, ReviewViewSet, SendCodeView, TitlesViewSet,
                    UserViewSet)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('titles', TitlesViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')

authurls = [
    path('signup/', SendCodeView.as_view(), name='send_code'),
    path('token/', GetTokenView.as_view(), name='token_obtain_pair'),
]

urlpatterns = [
    path('auth/', include(authurls)),
    path('', include(router.urls)),
]
