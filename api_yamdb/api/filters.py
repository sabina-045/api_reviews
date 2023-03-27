from django_filters import rest_framework as filter
from reviews.models import Title


class SlugFilterInFilter(filter.BaseInFilter, filter.CharFilter):
    pass


class TitleFilter(filter.FilterSet):
    genre = SlugFilterInFilter(fields_name='genre__slug', lookup_expr='in')

    class Meta:
        Model = Title
        fields = ['genre']
