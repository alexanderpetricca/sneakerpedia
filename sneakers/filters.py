import django_filters

from django.db.models import Q

from sneakers.models import Sneaker


class SneakerFilter(django_filters.FilterSet):

    search = django_filters.CharFilter(method='custom_search_filter', label='search')

    class Meta:
        model = Sneaker
        fields = [
            'brand', 
            'designer', 
            'year_released',
        ]


    def custom_search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(designer__icontains=value) |
            Q(brand__name__icontains=value)
        ).distinct()