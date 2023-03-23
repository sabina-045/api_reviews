from django.db import models


class Genre(models.Model):
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
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        related_name='category',
        verbose_name='Категория произведения',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
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
