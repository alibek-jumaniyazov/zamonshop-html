from products.models import Category

def categories(request):
    return {'category': Category.objects.filter(parent=None)}

