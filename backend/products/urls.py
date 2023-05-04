from django.urls import path, include

from .views import products ,productCategory
app_name = "products"




urlpatterns = [
    path('detail/', products, name="detail"),
    path('category/', productCategory, name="category"),
]
