from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from django.core.cache import cache
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

from sneakers.models import Brand, Sneaker
from sneakers.filters import SneakerFilter
from sneakers.forms import CreateSneakerForm, UpdateSneakerForm, DeleteSneakerForm
from sneakers.utils import get_active_filters
from core.utils import get_safe_next_url


def home_page_view(request):
    """
    Fetches brands and their associated sneakers, grouped and sorted.
    """

    brands_with_sneakers = cache.get('brands_with_sneakers')
    
    if not brands_with_sneakers:
        brands_with_sneakers = Brand.objects.filter(
            sneaker__isnull=False
        ).distinct().order_by('name')

        brands_with_sneakers = brands_with_sneakers.prefetch_related(
            Prefetch(
                'sneaker_set',
                queryset=Sneaker.objects.filter(deleted=False).order_by('name'),
                to_attr='sneakers',
            )
        )
        timeout_period = 60*60
        cache.set('brands_with_sneakers', brands_with_sneakers, timeout=timeout_period)    

    context = {
        'brands': brands_with_sneakers,
    }

    return render(request, 'sneakers/home.html', context)


def query_view(request):
    """
    Queries sneakers and displays results, based off user input.
    """
    
    base_qs = Sneaker.objects.filter(deleted=False)
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
    
    sneaker = get_object_or_404(
        Sneaker.objects.select_related('brand'), 
        id=pk, 
        deleted=False,
    )

    context = {
        'sneaker': sneaker,
    }

    return render(request, 'sneakers/detail.html', context)


@login_required
@permission_required('sneakers.add_sneaker', raise_exception=True)
def create_sneaker_view(request):
    """
    Renders create sneaker form on GET, and attempts to create it on POST.
    """
    
    form = CreateSneakerForm()

    if request.method == 'POST':
        form = CreateSneakerForm(request.POST)
        if form.is_valid():
            new_sneaker = form.save(commit=False)
            new_sneaker.created_by = request.user
            new_sneaker.save()

            next = get_safe_next_url(request, 'home')
            return redirect(next)
        
    context = {
        'form': form,
    }

    return render(request, 'sneakers/manage/create_sneaker.html', context)


@login_required
@permission_required('sneakers.change_sneaker', raise_exception=True)
def update_sneaker_view(request, pk):
    """
    Renders update sneaker form on GET, and attempts to update it on POST.
    """    
    
    sneaker = get_object_or_404(Sneaker, id=pk)
    form = UpdateSneakerForm(instance=sneaker)

    if request.method == 'POST':
        form = UpdateSneakerForm(request.POST, instance=sneaker)
        if form.is_valid():
            updated_sneaker = form.save(commit=False)
            updated_sneaker.last_updated_by = request.user
            updated_sneaker.save()

            next = get_safe_next_url(request, 'home')
            return redirect(next)
        
    context = {
        'form': form,
        'sneaker': sneaker
    }

    return render(request, 'sneakers/manage/update_sneaker.html', context)


@login_required
@permission_required('sneakers.delete_sneaker', raise_exception=True)
def delete_sneaker_view(request, pk):
    """
    Renders delete sneaker confirm on GET, and attempts to delete it on POST.
    """    
    
    sneaker = get_object_or_404(Sneaker, id=pk)
    form = DeleteSneakerForm(request.POST or None)

    if request.method == 'POST':
        success, msg = sneaker.soft_delete(request.user)

        if success:
            next = get_safe_next_url(request, 'home')
            return redirect(next)
        else:
            form.add_error(None, msg)
    
    context = {
        'sneaker': sneaker,
        'form': form,
    }

    return render(request, 'sneakers/manage/delete_sneaker.html', context)