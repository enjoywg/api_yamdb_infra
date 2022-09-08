from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
)


class User(AbstractUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_superuser:
            self.role = 'admin'

    role = models.CharField(
        choices=ROLES,
        default='user',
        max_length=20
    )
    bio = models.TextField(
        'Biography',
        blank=True,
    )

    @property
    def is_moderator(self):
        return self.role == ROLES[1][0]

    @property
    def is_admin(self):
        return self.role == ROLES[2][0]

    class Meta:
        ordering = ['username']


class Category(models.Model):
    """Создание модели Category."""
    name = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField(max_length=50, blank=False, null=False)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        """Метод str возвращает название категории."""
        return self.name


class Genre(models.Model):
    """Создание модели Genre."""
    name = models.CharField(max_length=256, blank=False)
    slug = models.SlugField(max_length=50, blank=False)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        """Метод str возвращает название жанра."""
        return self.name


class Title(models.Model):
    """Создание модели Title."""
    name = models.CharField(max_length=256, blank=False)
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        related_name='title',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle'
    )

    def __str__(self):
        return self.name[:15]

    class Meta:
        ordering = ['name']


class GenreTitle(models.Model):
    """Создание модели для связывания title_id и genre_id."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        """Метод str возвращает жанры произведения."""
        return f'{self.title} - {self.genre}.'


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(validators=[
        MaxValueValidator(10, message='Рейтинг не должен быть больше 10'),
        MinValueValidator(1, message='Рейтинг не должен быть ниже 1')
    ])
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'),
        ]
        ordering = ['id']

    def __str__(self):
        return self.text[:15]


class Comments(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ['id']
