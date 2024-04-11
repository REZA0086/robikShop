from django.contrib import admin
from main.models import *


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','image', 'price')

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('product','value')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('product','image')