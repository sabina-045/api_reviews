from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .serializers import ReviewSerializer, CommentSerializer
from reviews.models import Title, Review


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
