import datetime as dt
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# ниже добавил импорты для User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
#

from .permissions import (
    AuthorOrAuthenticatedOrReadOnly, ModeratorOnly,
    ReadOrAdminOnly, ReadOnly)
from .serializers import (
    CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer,
    TitleSerializer, UserSerializer,
    TitleReadOnlySerializer, TokenSerializer)
from reviews.models import Category, Genre, Review, Title
from users.models import CustomUser


class UserViewSet(ModelViewSet):
    """CRUD for user."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = IsAuthenticated
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
        permission_classes=IsAuthenticated
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

@api_view(['POST'])
@permission_classes([AllowAny, ])
def send_confirmation_code(request):
    """Отправка письма с кодом подтверждения."""
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        CustomUser,
        username=serializer.validated_data["username"]
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="YaMDb регистрация",
        message=f"YaMDb код подтверждения: {confirmation_code}",
        from_email=None,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([AllowAny])
def get_jwt_token(request):
    """Сравнить код подтвержденя и получить токен."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        CustomUser,
        username=serializer.validated_data["username"]
    )

    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreViewSet(ModelViewSet):
    """Получение списка жанров произведений.
    Создание, редактирование, удаление отдельных объектов админом."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser|ReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class CategoryViewSet(ModelViewSet):
    """Получение списка категорий.
    Создание, редактирование, удаление отдельных объектов админом."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser|ReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class TitleViewSet(ModelViewSet):
    """Получение списка произведений.
    Создание, редактирование,
    удаление отдельной записи о произвед."""
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    # queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminUser|ReadOnly]

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return TitleReadOnlySerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    """Получение списка отзывов.
    Получение, создание, редактирование,
    удаление отдельного отзыва."""
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrAuthenticatedOrReadOnly,)

    def get_permissions(self):
        """Разрешение анонимам получать информацию
        об отдельном объекте. Разрешение модератору
        удалять или редактировать отд. объект."""
        if self.action == 'retrieve':

            return (AllowAny(),)

        if self.request.user.is_moderator and self.action == (
            'update' or 'partial_update' or 'destroy'
        ):
            return (ModeratorOnly(),)

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
    permission_classes = (AuthorOrAuthenticatedOrReadOnly,)

    def get_permissions(self):
        """Разрешение анонимам получать информацию
        об отдельном объекте.Разрешение модератору
        удалять или редактировать отд. объект."""
        if self.action == 'retrieve':

            return (AllowAny(),)

        if self.request.user.is_moderator and self.action == (
            'update' or 'partial_update' or 'destroy'
        ):
            return (ModeratorOnly(),)

        return super().get_permissions()

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))

        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))

        return serializer.save(author=self.request.user,
                               review_id=review.id)
