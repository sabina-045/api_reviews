from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import filters

from reviews.models import Category, Genre, Title
from api.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer
)
from api.permissions import ReadOnly
import datetime as dt


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAdminUser|ReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser|ReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [permissions.IsAdminUser|ReadOnly]
