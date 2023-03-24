from rest_framework import permissions
from rest_framework import serializers
from rest_framework import filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import datetime as dt
from rest_framework import status
from reviews.models import Category, Genre, Title, Title, Review
from api.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer,
    ReviewSerializer, CommentSerializer, UserSerializer
)
from api.permissions import ReadOnly, AdminOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import CustomUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action


class UserViewSet(ModelViewSet):
    """CRUD for user."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, AdminOnly]
    pagination_class = PageNumberPagination
    # filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['get', 'put', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """Дополнительный маршрут 'me'."""
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)

            return Response(serializer.data)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)

        return Response(serializer.data)


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
