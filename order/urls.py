from django.urls import path
from order import views

app_name = "order"

urlpatterns = [
    path('order/', views.OrderView.as_view(), name='order'),
    path('orders/', views.add_product_to_order, name='add_orders'),
    path('remove_order/', views.remove_from_cart, name='remove_order'),
    path('add_order/', views.add_from_cart, name='add_from_cart'),
    path('request-payment/', views.request_payment, name='request_payment'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('btn_plus/<order_id>/', views.btn_plus, name='btn_plus'),
    path('btn_minus/<order_id>/', views.btn_minus, name='btn_minus'),
    path('btn_delete/<order_id>/', views.btn_delete, name='btn_delete'),
    path('add_address/', views.AddAddress.as_view(), name='add_address')

]
