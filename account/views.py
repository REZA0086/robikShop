from django.conf import settings
from django.contrib.auth import login
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.generic import View
from account.models import User
from account.forms import LoginForm, RegisterForm


# Create your views here.
def media_admin(request):
    return {'media_url': settings.MEDIA_URL, }

class LoginView(View):
    template_name = 'blog/login.html'

    def get(self, request):
        login_form = LoginForm()
        context = {
            'media_url': settings.MEDIA_URL,
            'form': login_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            user = User.objects.filter(username=user_name).first()
            if user is not None:
                if not user.is_active:
                    return JsonResponse({
                        'status': 'name error'
                    })
                else:
                    is_password = user.check_password(login_form.cleaned_data['password'])
                    if is_password:
                        login(request, user)
                        return redirect(reverse('blog:index'))
                    else:
                        return JsonResponse({
                            'status': 'pass error'
                        })
            else:
                return JsonResponse({
                    'status': 'not_authenticated'
                })

        context = {
            'media_url': settings.MEDIA_URL,
            'form': login_form
        }
        return render(request, self.template_name, context)


class RegisterView(View):
    template_name = 'blog/register.html'

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {
            'media_url': settings.MEDIA_URL,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user_email = form.cleaned_data.get('email')
            user_password = form.cleaned_data.get('password')

            user = User.objects.filter(email__iexact=user_email).exists()
            if user:
                form.add_error('email', 'ایمیل تکراری می باشد')
            else:
                new_user = User(
                    email=user_email,
                    is_active=False,
                    username=username,
                    email_active_code=get_random_string(72),
                )
                new_user.set_password(user_password)
                new_user.save()

                return redirect(reverse('account:login'))

        context = {
            'form': form
        }

        return render(request, self.template_name, context)





