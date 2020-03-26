import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
# Create your views here.

from django.contrib.auth.models import User
from main.models import Listing, Group
from main.models import LOCATION_CHOICES


@api_view(['GET',])
def get_listings(request):
    listings = [l.to_dict() for l in Listing.objects.all()]
    return Response(listings, status=status.HTTP_200_OK)

@api_view(['GET',])
def get_groups(request):
    groups = [g.to_dict() for g in Group.objects.all()]
    return Response(groups, status=status.HTTP_200_OK)

@api_view(['POST',])
def add_listing(request):
    json_data = request.data
    listing = Listing()
    listing.lister = User.objects.get(pk=json_data['lister'])
    listing.to_location = json_data['to_location']
    listing.from_location = json_data['from_location']
    listing.start = datetime.datetime.fromisoformat(json_data['start'])
    listing.end = datetime.datetime.fromisoformat(json_data['end'])
    listing.save()
    return Response(listing.to_dict(), status=status.HTTP_201_CREATED)

@api_view(['GET'])
def user_listing(request):
    user = request.user
    my_listing = [l.to_dict() for l in user.listings.all()]
    return Response(my_listing,status=status.HTTP_200_OK)

@api_view(['GET'])
def get_empty_group(request):
    to_location = request.GET.get('to_location')
    from_location = request.GET.get('from_location')

    allowed_loc = [x[0] for x in LOCATION_CHOICES]
    #checking whether the locations are allowed

    if (to_location not in allowed_loc ||from_location not in allowed_loc ):
        return Response('Location is invalid',status=status.HTTP_400_BAD_REQUEST)
    else :
        validated_to = to_location
        validated_from = from_location

    empty_groups = [g.to_dict() for g in Group.get.fav_groups(to_location=validated_to,from_location=validated_from)]
    
    return Response(empty_groups,status=status.HTTP_200_OK)

