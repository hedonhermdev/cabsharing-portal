import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

from django.contrib.auth.models import User
from main.models import Listing, Group
from main.models import LOCATION_CHOICES

from main.utils import find_num_hours_in_overlap, find_overlap_range

import logging
import sys

viewlog = logging.getLogger("viewlog")


@api_view(
    ["GET",]
)
@permission_classes(
    [IsAuthenticated,]
)
def get_listings(request):
    print(request.user)
    listings = [l.to_dict() for l in Listing.objects.all()]
    viewlog.debug(f"{request.path}: ALL LISTINGS {listings}")
    return Response(listings, status=status.HTTP_200_OK)


@api_view(
    ["GET",]
)
@permission_classes(
    [IsAuthenticated,]
)
def get_groups(request):
    groups = [g.to_dict() for g in Group.objects.all()]
    viewlog.debug(f"{request.path}: GROUPS {groups}")
    return Response(groups, status=status.HTTP_200_OK)


@api_view(
    ["POST",]
)
@permission_classes(
    [IsAuthenticated,]
)
def add_listing(request):
    json_data = request.data

    listing = Listing()
    listing.lister = request.user
    listing.to_location = json_data["to_location"]
    listing.from_location = json_data["from_location"]
    listing.start = datetime.datetime.fromisoformat(json_data["start"])
    listing.end = datetime.datetime.fromisoformat(json_data["end"])
    listing.save()

    viewlog.debug(f"{request.path}: NEW LISTING {listing.to_dict()}")
    return Response(listing.to_dict(), status=status.HTTP_201_CREATED)

@api_view(
    ["POST",]
)
@permission_classes(
    [IsAuthenticated,]
)
def create_new_group(request,listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        viewlog.error("{request.path}: Listing with PK {listing_id} does not exist")
        return Response({'error': "Listing not found"}, status=status.HTTP_404_NOT_FOUND)

    if listing.group is not None :
        viewlog.error("{request.path}: Listing already in a Group")
        return Response({'error':"Listing is already in a group"},status=status.HTTP_400_BAD_REQUEST) 

    if listing.lister != request.user :
        viewlog.error("{request.path}: Only lister of a listing can create a group for listing")
        return Response({'error':"Only lister can create a group for a listing"},status=status.HTTP_400_BAD_REQUEST)

    group = Group()
    group.start = listing.start
    group.end = listing.end
    group.to_location = listing.to_location
    group.from_location = listing.from_location

    group.save()
    
    group.members.add(listing)

    group.save()

    return Response(group.to_dict(),status=status.HTTP_201_CREATED)

@api_view(
    ["GET",]
)
@permission_classes(
    [IsAuthenticated,]
)
def get_potential_groups(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        viewlog.error("{request.path}: Listing with PK {listing_id} does not exist")
        return Response({'error': "Listing not found"}, status=status.HTTP_404_NOT_FOUND)

    listing_range = (listing.start, listing.end)

    potential_groups = Group.objects.groups_by_dest(to_location=listing.to_location, from_location=listing.from_location)

    overlap_func = lambda g: find_num_hours_in_overlap((g.start, g.end), listing_range)

    potential_groups = list(filter(overlap_func, potential_groups))
    potential_groups.sort(key=overlap_func)
    potential_groups.reverse()
    payload = [g.to_dict() for g in potential_groups]
    return Response(payload, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes(
    [IsAuthenticated,]
)
def user_listings(request):
    user = request.user
    my_listing = [l.to_dict() for l in user.listings.all()]
    return Response(my_listing, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes(
    [IsAuthenticated,]
)
def add_to_group(request, group_id):
    data = request.data
    
    try:
        group = Group.objects.get(pk=group_id)
    except Group.DoesNotExist:
        viewlog.error("{request.path}: Group with PK {listing_id} does not exist")
        return Response({'error': "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        
    listing = Listing.objects.get(pk=data['listing_pk'])
    
    listing.group = group

    listing.save()

    group_range = (group.start, group.end)
    listing_range = (listing.start, listing.end)

    overlap_range = find_overlap_range(group_range, listing_range)
    
    group.start = overlap_range[0]
    group.end = overlap_range[1]

    logging.info("{request.path}: LISTING {listing.to_dict()} ADDED TO {group.to_dict()}")

    return Response(group.to_dict(), status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def listing_detail(request, id):
    try:
        required_listing = Listing.objects.get(pk=id)
    except Listing.DoesNotExist:
        return Response("Listing not found", status=status.HTTP_404_NOT_FOUND)

    return Response(required_listing.to_dict(), status=status.HTTP_200_OK)


@api_view(["GET"])
def group_detail(request, id):
    try:
        required_group = Group.objects.get(pk=id)
    except Group.DoesNotExist:
        return Response("Group not found", status=status.HTTP_404_NOT_FOUND)

    return Response(required_group.to_dict(), status=status.HTTP_200_OK)

