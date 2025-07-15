from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from django.views.decorators.cache import cache_page

from sneakers.models import Brand, Sneaker
from sneakers.filters import SneakerFilter
from sneakers.utils import get_active_filters


@cache_page(60 * 60)
def home_page_view(request):
    """
    Fetches brands and their associated sneakers, grouped and sorted.
    """

    brands_with_sneakers = Brand.objects.filter(
        sneaker__isnull=False
    ).distinct().order_by('name')

    brands_with_sneakers = brands_with_sneakers.prefetch_related(
        Prefetch(
            'sneaker_set',
            queryset=Sneaker.objects.order_by('name'),
            to_attr='sneakers',
        )
    )

    context = {
        'brands': brands_with_sneakers,
    }

    return render(request, 'sneakers/home.html', context)


def query_view(request):
    """
    Queries sneakers and displays results, based off user input.
    """
    
    base_qs = Sneaker.objects.all()
    sneaker_filter = SneakerFilter(request.GET, queryset=base_qs)
    filtered_qs = sneaker_filter.qs.select_related('brand').order_by('name')

    active_filters = get_active_filters(sneaker_filter.form)

    context = {
        'sneakers': filtered_qs,
        'sneaker_filter': sneaker_filter,
        'active_filters': active_filters,
    }

    return render(request, 'sneakers/query.html', context)


def detail_view(request, pk):
    """
    Fetches specific sneaker and renders detail page.
    """
    
    sneaker = get_object_or_404(Sneaker, id=pk)

    context = {
        'sneaker': sneaker,
    }

    return render(request, 'sneakers/detail.html', context)