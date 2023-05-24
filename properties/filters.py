import django_filters
from .models import OffPlansProperty, News


class OffPlansPropertyFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='min_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='max_price', lookup_expr='lte')
    developer = django_filters.CharFilter(lookup_expr='icontains')
    handover_date = django_filters.DateFilter(field_name='handover_date', lookup_expr='exact')

    class Meta:
        model = OffPlansProperty
        fields = ['title', 'min_price', 'max_price', 'developer', 'handover_date']


class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    subtitle = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = News
        fields = ['title', 'subtitle']