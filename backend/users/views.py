import random
import time
import re
from django.db import IntegrityError
from django.forms import ValidationError

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import auth, messages
from users.forms import UserProfileForm

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

def is_valid_uzbek_phone_number(phone_number):
    pattern = r'^\d{9}$'
    return bool(re.match(pattern, phone_number))



# @login_required
def profil(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {

        "title": "Profile",
        "form": form,
    }
    return render(request , 'users/profil.html')


@login_required
def myproduct(request):
    return render(request , 'users/myproduct.html')


@login_required
def mylocation(request):
    return render(request , 'users/mylocation.html')


# otp login
def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        if is_valid_uzbek_phone_number(phone_number):

        
            profile = Profile.objects.filter(phone_number=phone_number).first()
            if not profile:
                return HttpResponseRedirect(reverse('users:registration'))


            session = SessionStore(request.session.session_key)
            last_otp_time = session.get('last_otp_time')
            current_time = time.time()
            
            if last_otp_time and current_time - last_otp_time < 60:
                messages.warning(request, '60 sekunddan oldin yana bir marta so\'rov yuborishingiz mumkin')
                return redirect('users:login')
            

            try:
                profile.otp = random.randint(1000, 9999)
                profile.save()
                print(profile)
            except ValidationError as e:
                print(e)

            message_handler = SendSmsApiWithEskiz(message=str(profile.otp), phone=phone_number)
            message_handler.send()
            

            session['last_otp_time'] = current_time
            session.save()

            return redirect(f'/users/otp/{profile.uid}')
        
        else:
            messages.warning(request, 'uzbek raqam kiriting!!!\n')

    return render(request, 'users/login.html')


def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("users:login"))


def registration(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        phone_number = request.POST.get("phone_number")
        if is_valid_uzbek_phone_number(phone_number):
            try:

                user = User.objects.create(username=username)
                profile = Profile.objects.create(user=user, phone_number=phone_number)

                return HttpResponseRedirect(reverse('users:login'))
            
            except IntegrityError:
                messages.warning(request, 'Bunay username mavjud!!!')
                
        else:
            messages.warning(request, 'uzbek raqam kiriting!!!')


    return render(request, 'users/registration.html')

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
