from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.contrib.auth import login
from django.db.models import Sum
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import View

from main.models import Product, Category, Feature, Gallery


def media_admin(request):
    return {'media_url': settings.MEDIA_URL, }


class IndexView(View):
    template_name = 'blog/index.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        product_sell = Product.objects.all().order_by('-order_count')

        context = {
            'media_url': settings.MEDIA_URL,
            'products': products,
            'product_sell': product_sell

        }
        return render(request, self.template_name, context)


class ProductView(View):
    template_name = 'blog/product.html'

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        features = Feature.objects.filter(product=product)
        gallery = Gallery.objects.filter(product=product)
        product.visited_count += 1
        product.save()
        context = {
            'product': product,
            'media_url': settings.MEDIA_URL,
            'features': features,
            'gallery': gallery
        }
        return render(request, self.template_name, context)


