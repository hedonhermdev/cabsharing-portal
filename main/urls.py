from django.urls import path

from .views import content, auth

urlpatterns = [
    path('api/get_listings', content.get_listings, name='get-listings'),
    path('api/get_groups/', content.get_groups, name='get-groups'),
    path('api/add_listing', content.add_listing, name='add-listing'),

    path('auth/login/', auth.login, name='auth-login')

]
