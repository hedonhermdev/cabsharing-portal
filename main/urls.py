from django.urls import path

from .views import content, auth

urlpatterns = [
    path('api/get_listings', content.get_listings, name='get-listings'),
    path('api/get_groups/', content.get_groups, name='get-groups'),
    path('api/add_listing', content.add_listing, name='add-listing'),
    path('api/create_new_group/<int:listing_id>',content.create_new_group,name='create-new-group'),
    path('api/get_potential_groups/<int:listing_id>', content.get_potential_groups, name='get-potential-groups'),
    path('api/add_to_group/<int:group_id>', content.add_to_group, name='add-to-group'),

    path('auth/login/', auth.login, name='auth-login'),
    path('auth/register/', auth.register, name='auth-register'),
]
