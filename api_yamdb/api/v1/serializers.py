from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import (ROLES, Category, Comments, Genre, Review, Title,
                            User)


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        required=True,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        lookup_field = 'slug'
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256, required=True)
    slug = serializers.SlugField(
        max_length=50,
        required=True,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        lookup_field = 'slug'
        model = Category
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )
    review = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Comments
        fields = "__all__"


class SendCodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='This username is already registered'
            )
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='This email is already registered'
            )
        ]
    )

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise serializers.ValidationError(
                f'You are not allowed to use "{data["username"]}" as '
                f'your username'
            )
        return data

    class Meta:
        fields = ('username', 'email')
        model = User


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='This username is already registered'
            )
        ]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='This email is already registered'
            )
        ]
    )
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User

    def validate_role(self, value):
        if value not in (role[0] for role in ROLES):
            raise serializers.ValidationError(
                'Role can be: user, moderator or admin'
            )
        return value


class MeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)
