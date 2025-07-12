from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView


@api_view(['GET'])
def test_authentication(request:Request, format=None):
    if request.user.is_authenticated:
        return Response({'message': 'You are logged in'}, status=status.HTTP_200_OK)
    return Response({'message': 'You are not logged in'},status=status.HTTP_403_FORBIDDEN)