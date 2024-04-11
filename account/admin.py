from django.contrib import admin

# Register your models here.
from django.contrib import admin
from account.models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')