from django.urls import path

from . import views


urlpatterns = [
    path('api/get_listings', views.get_listings, name='get-listings'),
    path('api/get_groups/', views.get_groups, name='get-groups'),
    path('api/add_listing', views.add_listing, name='add-listing')
]
