import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Category, Asset
from .forms import AssetSubmitForm


def map_view(request):
    categories = Category.objects.all()
    return render(request, 'assets/map.html', {'categories': categories})


def asset_geojson(request):
    category_slug = request.GET.get('category')
    qs = Asset.objects.filter(status='active').select_related('category')
    if category_slug:
        qs = qs.filter(category__slug=category_slug)

    features = []
    for asset in qs:
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(asset.longitude), float(asset.latitude)],
            },
            'properties': {
                'id': asset.id,
                'name': asset.name,
                'category': asset.category.name,
                'category_slug': asset.category.slug,
                'category_color': asset.category.color,
                'category_icon': asset.category.icon,
                'description': asset.description,
                'address': asset.address,
                'phone': asset.phone,
                'website': asset.website,
                'hours': asset.hours,
                'verified': asset.verified,
                'tags': asset.tag_list(),
            }
        })

    return JsonResponse({'type': 'FeatureCollection', 'features': features})


def asset_list(request):
    category_slug = request.GET.get('category', '')
    search = request.GET.get('q', '')

    categories = Category.objects.all()
    assets = Asset.objects.filter(status='active').select_related('category')

    if category_slug:
        assets = assets.filter(category__slug=category_slug)
    if search:
        assets = assets.filter(name__icontains=search) | assets.filter(description__icontains=search)

    assets = assets.order_by('name')

    return render(request, 'assets/list.html', {
        'assets': assets,
        'categories': categories,
        'active_category': category_slug,
        'search': search,
    })


def asset_detail(request, pk):
    asset = get_object_or_404(Asset, pk=pk, status='active')
    return render(request, 'assets/detail.html', {'asset': asset})


def submit_asset(request):
    if request.method == 'POST':
        form = AssetSubmitForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.status = 'pending'
            asset.save()
            messages.success(request, 'Thank you! Your submission is under review and will appear on the map once approved.')
            return redirect('submit_success')
    else:
        form = AssetSubmitForm()

    categories = Category.objects.all()
    return render(request, 'assets/submit.html', {'form': form, 'categories': categories})


def submit_success(request):
    return render(request, 'assets/submit_success.html')
