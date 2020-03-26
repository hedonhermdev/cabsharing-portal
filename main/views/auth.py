from google.oauth2 import id_token as googleIdToken
from google.auth.transport import requests as google_requests

from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST',])
def login(request):
    try:
        id_token = request.data['id_token']
    except KeyError:
        return Response({'error': 'No id_token provided'}, status=status.HTTP_403_FORBIDDEN)

    id_info = googleIdToken.verify_oauth2_token(id_token, google_requests.Request())

    if id_info['iss'] not in ["accounts.google.com", "https://accounts.google.com"]:
        return Response({'error': "Not a valid Google account"}, status=status.HTTP_403_FORBIDDEN)
    
    hd = getattr(id_info, 'hd', '')
    if hd != 'pilani.bits-pilani.ac.in':
        return Response({'error': 'Not a valid BITS Mail account. '}, status=status.HTTP_403_FORBIDDEN)
    return Response({}, status=status.HTTP_200_OK)

