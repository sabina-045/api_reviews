from rest_framework import permissions
from rest_framework import serializers
from rest_framework import filters
from django.shortcuts import get_object_or_404
import datetime as dt
from reviews.models import Category, Genre, Title, Title, Review
from api.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer,
    ReviewSerializer, CommentSerializer
)
from api.permissions import ReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
 

class GenreViewSet(ModelViewSet):
    """Получение списка жанров произведений.
    Создание, редактирование, удаление отдельных объектов админом."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAdminUser|ReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class CategoryViewSet(ModelViewSet):
    """Получение списка категорий.
    Создание, редактирование, удаление отдельных объектов админом."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser|ReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class TitleViewSet(ModelViewSet):
    """Получение списка произведений.
    Получение, создание, редактирование,
    удаление отдельной записи о произвед."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [permissions.IsAdminUser|ReadOnly]


class ReviewViewSet(ModelViewSet):
    """Получение списка отзывов.
    Получение, создание, редактирование,
    удаление отдельного отзыва."""
    serializer_class = ReviewSerializer
    # permission_classes =

    def get_permissions(self):
        """Разрешение анонимам получать информацию
        об отдельном объекте."""
        if self.action == 'retrieve':

            return (AllowAny(),)

        return super().get_permissions()

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        return serializer.save(author=self.request.user,
                               title_id=title.id)


class CommentViewSet(ModelViewSet):
    """Получение списка комментариев к отзыву.
    Получение, создание, редактирование,
    удаление отдельного комментария."""
    serializer_class = CommentSerializer
    # permission_classes =

    def get_permissions(self):
        """Разрешение анонимам получать информацию
        об отдельном объекте."""
        if self.action == 'retrieve':

            return (AllowAny(),)

        return super().get_permissions()

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))

        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))

        return serializer.save(author=self.request.user,
                               review_id=review.id)
