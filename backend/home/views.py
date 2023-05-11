from django.shortcuts import render

from .models import Banner
from products.models import Category

# Create your views here.


def index(request):

    categories = Category.objects.filter(children=None)

    context = {
        "categories": categories,
        "banner": Banner.objects.all().order_by("-id")[:5]
    }

    return render(request, 'home/index.html', context)
    

def chat(request):

    return render(request, 'chat/chat.html')

