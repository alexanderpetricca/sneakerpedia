from django.shortcuts import render
from django.db.models import Prefetch

from sneakers.models import Brand, Sneaker


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
            to_attr='sneakers'
        )
    )

    context = {
        'brands': brands_with_sneakers,
    }

    return render(request, 'sneakers/home.html', context)
