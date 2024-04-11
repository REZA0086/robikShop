from django.contrib import admin
from order.models import *
# Register your models here.
@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ('user','is_paid','payment_date')

@admin.register(OrderDetail)
class OrderDetail(admin.ModelAdmin):
    list_display = ('product','order','count')