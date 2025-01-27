from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/<int:product_id>/', views.ProductView.as_view(), name='product'),
]