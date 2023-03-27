import datetime as dt
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Genre, Category, Title, Review, Comment
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор кастомного юзера"""
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ['password', ]
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate_username(self, value):
        """Валидация юзернейма."""
        if value.lower() == 'me':
            raise serializers.ValidationError('Нельзя использовать логин "me"')
        return value


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
    )

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise serializers.ValidationError('Нельзя использовать логин "me"')
        return data

    class Meta:
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset = Genre.objects.all(),
        many = True,
        slug_field='slug',
    )
    category = serializers.SlugRelatedField(
        queryset = Category.objects.all(),
        many=False,
        slug_field='slug',
    )
    class Meta:
        model = Title
        fields = '__all__'

    def validate(self, data):
        year_now = dt.datetime.now().year
        if data['year'] > year_now:
            raise serializers.ValidationError(
                'Нельзя публиковать не вышедшие произведения'
            )
        return data


class TitleReadOnlySerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True,
    )
    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('pub_date', 'title',)


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('__all__')
        read_only_fields = ('pub_date', 'review',)
