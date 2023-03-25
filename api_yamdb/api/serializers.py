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
        read_only_fields = ['password', 'role']
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate_username(self, value):
        """Валидация юзернейма."""
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f'Имя {value} не подходит.')
        return value


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

    class Meta:
        model = Title
        fields = '__all__'

    # Не проверял. Будет ли работать?
    """
    def create(self, validated_data):
        year_now = dt.datetime.today().year
        year_data = validated_data.get('year')
        if year_data <= year_now:
            return Title.objects.create(**validated_data)
        else:
            raise serializers.ValidationError(
                'Нельяз публиковать не вышедшие произведения'
            )
    """


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('pub_date',)


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('__all__')
        read_only_fields = ('pub_date',)
