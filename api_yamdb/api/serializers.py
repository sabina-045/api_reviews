import datetime as dt
from rest_framework import serializers

from reviews.models import Genre, Category, Title


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
