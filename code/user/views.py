from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from base_app import csrf

class Signup(APIView):
  authentication_classes = (csrf.CsrfExemptSessionAuthentication, csrf.BasicAuthentication)

  def get(self, request):
    if request.user.is_authenticated:
      return Response(data="Authenticated", status=status.HTTP_200_OK)
    return Response(status=status.HTTP_204_NO_CONTENT)

  def post(self, request, *args, **kwargs):
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    email = request.data.get('email', '')
    print('creating user')
    user = User.objects.create_user(username=username, email=email, password=password)
    print(user)
    print('saved user')
    return Response(data="created user", status=status.HTTP_201_CREATED)
      
class Signin(APIView):
  authentication_classes = (csrf.CsrfExemptSessionAuthentication, csrf.BasicAuthentication)

  def get(self, request):
    if request.user.is_authenticated:
      return Response(data="Authenticated", status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


  def post(self, request):
    username = request.data.get('username', '')
    password = request.data.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None:
      login(request, user)
      return Response(data="Authenticated", status=status.HTTP_200_OK)
    else:
      return Response(data="invalid signin", status=status.HTTP_401_UNAUTHORIZED)
