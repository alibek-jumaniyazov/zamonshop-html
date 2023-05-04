from django.urls import path, include

from .views import products ,product
app_name = "products"




urlpatterns = [
    path('detail/', products, name="detail"),
]
