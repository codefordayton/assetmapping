from django.urls import path
from django.http import JsonResponse
from . import views


def health(request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('health/', health, name='health'),
    path('', views.map_view, name='map'),
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/<int:pk>/', views.asset_detail, name='asset_detail'),
    path('submit/', views.submit_asset, name='submit'),
    path('submit/thanks/', views.submit_success, name='submit_success'),
    path('api/assets.geojson', views.asset_geojson, name='asset_geojson'),
]
