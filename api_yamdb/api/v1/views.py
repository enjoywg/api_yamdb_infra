from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from reviews.models import Category, Comments, Genre, Review, Title, User

from .filters import Titlefilter
from .mixins import CreateDestroyListViewSet
from .permissions import IsAdmin, IsAdminOrReadOnly, OwnerOrReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, GetTokenSerializer, MeSerializer,
                          ReviewSerializer, SendCodeSerializer,
                          TitleReadSerializer, TitleSerializer, UserSerializer)


class SendCodeView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        user = User.objects.get(username=request.data.get('username'))
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Yamdb: Confirm your registration',
            message=f'Confirmation code: {confirmation_code}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(
            User,
            username=request.data.get('username')
        )

        if default_token_generator.check_token(
                user, request.data.get('confirmation_code')
        ):
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )

        return Response({'error': 'Confirmation code is not valid'},
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = PageNumberPagination
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        detail=False
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = MeSerializer(
                request.user, data=request.data, partial=True
            )
            if not serializer.is_valid():
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')).order_by('name')
    lookup_field = 'id'
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = Titlefilter
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        if Review.objects.all().filter(
                author=self.request.user,
                title=title).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение'
            )
        serializer.save(author=self.request.user, title=title)


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (OwnerOrReadOnly,)

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        title_id = self.kwargs.get('title_id')
        current_review = get_object_or_404(
            Review,
            id=review_id,
            title_id=title_id
        )
        serializer.save(author=self.request.user, review=current_review)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        title_id = self.kwargs.get('title_id')
        if get_object_or_404(Review, id=review_id, title_id=title_id):
            return Comments.objects.filter(review=review_id)
