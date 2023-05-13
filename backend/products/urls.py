from django.urls import path, include

from .views import products, basket, basket_add, basket_remove, productCategory
app_name = "products"




urlpatterns = [
    path('detail/', products, name="detail"),
    path('savat/', basket, name="savat"),
    path('basket/<int:product_id>', basket_add, name="basketadd"),
    path('basket/<int:basket_id>', basket_remove, name="basketremove"),
    path('category/', productCategory, name="category"),
]
