import random
import time
from django.db import IntegrityError
from django.forms import ValidationError

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import auth, messages

from users.mixins import SendSmsApiWithEskiz


from .serializers import UserSerializer, MyTokenObtainPairSerializer

from .models import User, Profile

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/users/token/',
        '/users/register/',
        '/users/token/refresh/'
    ]
    return Response(routes)

@csrf_exempt
def login_otp_view(request):

    if request.method == 'POST':

        phone_number = request.POST.get('phone_number')
        otp = request.POST.get('otp')

        profile = Profile.objects.filter(phone_number=phone_number).first()
        
        if not profile:
            return JsonResponse({'go_register': 'Royxatdan otmagan foydalanuvchu.'}, status=401)

        # if profile.otp == otp:
        #     return JsonResponse({"success": True})

        session = SessionStore(request.session.session_key)
        current_time = time.time()
        last_otp_time = session.get('last_otp_time')

        if last_otp_time and current_time - last_otp_time < 60:
            return JsonResponse({'go_login': '60 sekunddan oldin yana bir marta so\'rov yuborishingiz mumkin'})

        try:
            profile.otp = random.randint(1000, 9999)
            profile.save()
        except ValidationError as e:
            print(e)

        message_handler = SendSmsApiWithEskiz(message=str(profile.otp), phone=phone_number)
        message_handler.send()

        session['last_otp_time'] = current_time
        session.save()

@csrf_exempt
def registration(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        phone_number = request.POST.get("phone_number")

        try:

            user = User.objects.create(username=username)
            profile = Profile.objects.create(user=user, phone_number=phone_number)

            return JsonResponse({"success": True})
        
        except IntegrityError:
            return JsonResponse({"error": "invalid profile"})


def otp(request, uid):
    if request.method == "POST":
        otp = request.POST.get('otp')
        profile = Profile.objects.get(uid = uid)
        if otp == profile.otp:
            auth.login(request, profile.user)
            # return HttpResponseRedirect(reverse('users:profile'))
        
        # return redirect(f'/users/otp/{uid}')
    return render(request, 'users/otp.html')

def profil(request):
    return render(request , 'users/profil.html')

def myproduct(request):
    return render(request , 'users/myproduct.html')

def mylocation(request):
    return render(request , 'users/mylocation.html')







# class UserSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegisterSerializer


# class UserRegistrationView(generics.CreateAPIView):
#     serializer_class = UserRegisterSerializer
#     permission_classes = (AllowAny,)


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

