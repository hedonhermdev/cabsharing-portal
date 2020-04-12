from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as googleIdToken
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.auth_helpers import generate_random_password, get_jwt_with_user
import logging
import sys


# Logging 
logging.basicConfig(filename='views.log', filemode='a', 
                             format='%(asctime)s %(levelname)s\t%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


@api_view(['POST',])
def login(request):
    try:
        id_token = request.data['id_token']
    except KeyError:
        return Response({'error': 'No id_token provided'}, status=status.HTTP_403_FORBIDDEN)

    id_info = googleIdToken.verify_oauth2_token(id_token, google_requests.Request())
    print(id_info)

    if id_info['iss'] not in ["accounts.google.com", "https://accounts.google.com"]:
        return Response({'error': "Not a valid Google account"}, status=status.HTTP_403_FORBIDDEN)
    
    email = id_info['email']

    hd = getattr(id_info, 'hd', email.split('@')[-1])
    if hd != 'pilani.bits-pilani.ac.in':
        logging.error(f"{request.path}: {email} is not a valid BITS Mail account")
        return Response({'error': '{email} is not a valid BITS Mail account'}, status=status.HTTP_403_FORBIDDEN)
    
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        logging.error(f"{request.path}: {email} is not registered.")
        return Response({'error': 'Account not found. You must register first. '}, status=status.HTTP_403_FORBIDDEN)

    token = get_jwt_with_user(user)

    logging.info(f"{request.path}: user {user.username} logged in. ")
    return Response({'token': token}, status=status.HTTP_200_OK)


@api_view(['POST',])
def register(request):
    try:
        id_token = request.data['id_token']
    except KeyError:
        logging.error(f"{request.path}: no id_token provided in request body. ")
        return Response({'error': 'No id_token provided'}, status=status.HTTP_403_FORBIDDEN)

    id_info = googleIdToken.verify_oauth2_token(id_token, google_requests.Request())

    if id_info['iss'] not in ["accounts.google.com", "https://accounts.google.com"]:
        return Response({'error': "Not a valid Google account"}, status=status.HTTP_403_FORBIDDEN)
    
    email = id_info['email']

    hd = getattr(id_info, 'hd', email.split('@')[-1])
    if hd != 'pilani.bits-pilani.ac.in':
        logging.error(f"{request.path}: {email} is not a valid BITS Mail account")
        return Response({'error': 'Not a valid BITS Mail account. '}, status=status.HTTP_403_FORBIDDEN)

    if User.objects.filter(email=email).count() != 0:
        logging.error("f{request.path}: user with email {email} already exists")
        return Response({'error': 'An account already exists. Try logging in instead. '}, status=status.HTTP_403_FORBIDDEN)

    user = User(username=email.split('@')[0], email=email) 
    user.set_password(generate_random_password())

    user.save()

    token = get_jwt_with_user(user)

    logging.info(f"{request.path}: created user with email {user.email}")
    return Response({'token': token, 'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)

