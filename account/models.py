from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/', verbose_name='عکس کاربر')
    email_active_code = models.CharField(max_length=100, verbose_name="کد فعالسازی ایمیل")
    address = models.CharField(max_length=200, verbose_name="آدرس", null=True, blank=True)

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.username
