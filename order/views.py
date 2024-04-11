import json
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from django.views import View
from order.forms import add_address
from order.models import *
from main.models import *

# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
phone = ''  # Optional

CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'


class OrderView(View):
    def get(self, request: HttpRequest):
        current_order = Order.objects.get(is_paid=False, user_id=request.user.id)
        discount_sum = 0
        for item in current_order.orderdetail_set.all():
            discount_sum += item.discount_price()
        price_sum = 0
        for item in current_order.orderdetail_set.all():
            price_sum += item.get_final_price()
        final_price = price_sum - discount_sum
        context = {
            'media_url': settings.MEDIA_URL,
            'order': current_order,
            'discount_sum': discount_sum,
            'price_sum': price_sum,
            'final_price': final_price
        }
        return render(request, 'blog/cart.html', context)


def add_product_to_order(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status': 'invalid_count'
        })
    if request.user.is_authenticated:
        product = Product.objects.filter(pk=product_id).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()

            if current_order_detail is not None:
                current_order_detail.count += int(count)
                current_order_detail.save()
            else:
                new_detail = OrderDetail(order_id=current_order.id, product_id=product_id,
                                         final_price=product.price * count, count=count)
                new_detail.save()
            return JsonResponse({
                'status': 'success'
            })

        else:
            return JsonResponse({
                'status': 'not_found'
            })
    else:
        return JsonResponse({
            'status': 'not_authenticated'
        })


def remove_from_cart(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))

    cart_item = OrderDetail.objects.filter(product_id=product_id).first()
    print(cart_item)
    if cart_item.count > 1:
        cart_item.count -= 1
        cart_item.save()
    else:
        cart_item.delete()

    total_price = cart_item.final_price * int(cart_item.count)
    return JsonResponse({
        'final_price': total_price
    })


def add_from_cart(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    cart_item = OrderDetail.objects.filter(product_id=product_id).first()
    print(cart_item)
    if cart_item.count >= 1:
        cart_item.count += 1
        cart_item.save()

    total_price = cart_item.final_price * int(cart_item.count)
    return JsonResponse({
        'final_price': total_price
    })


@login_required
def request_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    final_price = current_order.calculate_total()
    if final_price == 0:
        return redirect(reverse('main:index'))

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": int(final_price / 10),
        "Description": description,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data

    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return redirect(ZP_API_STARTPAY + str(response['Authority']))
            else:
                return JsonResponse({'status': 'pay error'})
        else:
            return JsonResponse({'status': 'pay error'})

    except requests.exceptions.Timeout:
        return JsonResponse({'status': 'pay error'})
    except requests.exceptions.ConnectionError:
        return JsonResponse({'status': 'pay error'})


def verify_payment(request: HttpRequest):
    current_order = Order.objects.get(is_paid=False)
    total_price = current_order.calculate_total_price()
    for order in current_order.orderdetail_set.all():
        if order.product.order_count is not None:
            order.product.order_count = int(order.product.order_count) + order.count
        else:
            order.product.order_count = order.count

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": int(total_price * 10),
        "Authority": request.GET.get('Authority'),
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        # current_order.is_paid = True
        # current_order.save()
        if response['Status'] == 100:
            return render(request, 'blog/payment_result.html',
                          {'status': f'تراکنش با موفقیت انجام شد'})
        else:
            current_order.is_paid = False
            return render(request, 'blog/payment_result.html', {'status': 'پرداخت ناموفق'})
    else:
        current_order.is_paid = False
        return render('blog/payment_result.html',{'status': 'nop'})


class CheckoutView(View):
    template_name = 'blog/checkout.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        current_order = Order.objects.get(is_paid=False, user_id=request.user.id)
        discount_sum = 0
        for item in current_order.orderdetail_set.all():
            discount_sum += item.discount_price()
        price_sum = 0
        for item in current_order.orderdetail_set.all():
            price_sum += item.get_final_price()
        final_price = price_sum - discount_sum

        context = {
            'media_url': settings.MEDIA_URL,
            'user': user,
            'order': current_order,
            'discount_sum': discount_sum,
            'price_sum': price_sum,
            'final_price': final_price

        }
        return render(request, self.template_name, context)


def btn_plus(request, order_id):
    order_detail = OrderDetail.objects.get(id=order_id)
    order_detail.count += 1
    order_detail.save()
    return redirect(reverse('order:order'))


def btn_delete(request, order_id):
    order_detail = OrderDetail.objects.get(id=order_id)
    order_detail.delete()
    return redirect(reverse('order:order'))


def btn_minus(request, order_id):
    order_detail = OrderDetail.objects.get(id=order_id)
    order_detail.count -= 1
    if order_detail.count < 1:
        order_detail.delete()
        return redirect(reverse('order:order'))
    order_detail.save()
    return redirect(reverse('order:order'))


class AddAddress(View):
    def get(self, request: HttpRequest):
        form = add_address()
        user = request.user
        context = {
            'form': form,
            'user': user
        }
        return render(request, 'blog/add_address.html', context)

    def post(self, request: HttpRequest):
        form = add_address(request.POST)
        user = request.user
        if form.is_valid():
            user.address = form.cleaned_data['address']
        user.save()
        return redirect(reverse('order:checkout'))
