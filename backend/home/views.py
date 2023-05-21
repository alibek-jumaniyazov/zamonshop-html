from django.shortcuts import render, get_object_or_404

from .models import Banner, SwipperBanner
from products.models import Category, Product

# Create your views here.


def index(request, cat_id=None):

    categories = Category.objects.filter(children=None)
    products = Product.objects.filter(category__id=cat_id) if cat_id else Product.objects.all().order_by("-id")[:10]

    context = {
        "categories": categories,
        "products": products,
        "banner": Banner.objects.all().order_by("-id")[:5],
        "swipe_banner": SwipperBanner.objects.all().order_by("-id")[:5],

    }

    return render(request, 'home/index.html', context)



def chat(request):
    return render(request, 'chat/chat.html')

