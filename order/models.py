from django.db.models import ForeignKey
from account.models import *
from main.models import *
from django_jalali.db import models as jmodels
import jdatetime


# Create your models here.
class Order(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="نام مشتری")
    is_paid = models.BooleanField(verbose_name="نهایی شده / نشده")
    payment_date = jmodels.jDateField(auto_now=True, verbose_name="تاریخ پرداخت", blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید کاربران"

    def calculate_total_price(self):
        discount_price = 0
        total = 0

        for order_detail in self.orderdetail_set.all():
            total += order_detail.product.price

        for order_detail in self.orderdetail_set.all():
            discount_price += ((order_detail.product.price * order_detail.product.discount) / 100) * order_detail.count

        final_price = total - discount_price

        return int(final_price)

    def calculate_total(self):
        total_amount = 0

        for order_detail in self.orderdetail_set.all():
            if self.is_paid:
                total_amount += order_detail.final_price
            else:
                total_amount += order_detail.product.price * order_detail.count - order_detail.discount_price()

        return int(total_amount)


class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, verbose_name="محصول سبد خرید")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, verbose_name="سبد خرید")
    final_price = models.IntegerField(verbose_name="قیمت نهایی تکی محصول", blank=True, null=True)
    count = models.IntegerField(verbose_name="تعداد")

    class Meta:
        verbose_name = "جزییات سبد خرید"
        verbose_name_plural = "لیست جزییات سبدهای خرید"

    def __str__(self):
        return str(self.order)

    def get_final_price(self):
        return self.product.price * self.count

    def discount_price(self):
        return self.get_final_price() * (self.product.discount / 100)

    def Final_Price(self):
        return self.get_final_price() - self.discount_price()
