from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import CustomUser


class Genre(models.Model):
    """Класс жанров."""
    name = models.CharField(
        'Название категории',
        blank=False,
        null=False,
        max_length=256,
    )
    slug = models.SlugField(
        blank=False,
        null=False,
        unique=True,
        verbose_name='URL',
        max_length=50,
    )

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """Класс категорий."""
    name = models.CharField(
        'Название категории',
        blank=False,
        null=True,
        max_length=256,
    )
    slug = models.SlugField(
        blank=False,
        null=False,
        unique=True,
        verbose_name='URL',
        max_length=50,
    )
    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Класс произведений."""
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name='category',
        verbose_name='Категория произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=False,
        through='GenreTitle',
        related_name='genre',
        verbose_name='Жанр произведения',
    )
    name = models.CharField(
        'Название произведения',
        max_length=256,
        blank=False,
        null=False,
    )
    year = models.IntegerField(
        'Год произведения',
        blank=False,
        null=False,
    )
    description = models.CharField(
        'Описание произведения',
        blank=True,
        null=True,
        max_length=256
    )
    rating = models.IntegerField(
        'Оценка произведения',
        null=True,
        default=0,
    )

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    """Класс связ. жанры и произв."""
    title= models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self) -> str:
        return f'Произведение: {self.title}, жанр: {self.genre}'


class Review(models.Model):
    """Класс отзывов к произведению."""
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(10)])
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title',],
                name='author_title'
            )
        ]


class Comment(models.Model):
    """Класс комментариев к отзыву."""
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
