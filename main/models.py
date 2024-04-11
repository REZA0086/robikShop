from django.db import models
from account.models import *
from django_jalali.db import models as jmodels
import jdatetime
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='دسته بندی',null=True,blank=True)
    logo = models.ImageField(upload_to='category/',verbose_name='عکس دسته بندی',null=True,blank=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name="دسته بندی محصول")
    image = models.ImageField(upload_to='product/', verbose_name="عکس محصول")
    name = models.CharField(max_length=250, verbose_name="نام محصول")
    price = models.DecimalField(max_digits=11, decimal_places=0, verbose_name="قیمت")
    discount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="تخفیف")
    created_time = jmodels.jDateField(null=True, blank=True, verbose_name="تاریخ ثبت محصول",
                                      default=jdatetime.datetime.today())
    order_count = models.IntegerField(default=0, verbose_name="تعداد فروش")
    visited_count = models.IntegerField(default=0, verbose_name="تعداد بازدید")
    description = models.TextField(verbose_name="توضیح محصول", null=True,blank=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

class Feature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="ویژگی محصول")
    value = models.CharField(max_length=250, verbose_name="مقدار ویژگی", null=True,blank=True)

class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=" محصول")
    image = models.ImageField(upload_to='gallery/', verbose_name="عکس محصول", null=True,blank=True)


