from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from . import views
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views


# router = routers.DefaultRouter()
# router.register(r'', views.UserSet)
# router.register(r'api/token/', "users")


app_name = 'users'

urlpatterns = [
    # path('', include(router.urls)),
    # path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/auth/register/', views.UserCreate.as_view(), name='register'),
    # path('register/', views.UserRegistrationView.as_view()),

    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('', views.profil , name="users"),
    path('myproduct/', views.myproduct, name="myproduct"),
    path('mylocation/' , views.mylocation , name="mylocation"),
    
]

