from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _


def index_view(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, _('You are logged in'))
            return redirect('home')
        else:
            messages.error(request, _('Please enter a correct username '
                                    'and password. Note that both fields '
                                      'may be case-sensitive.'))

    return render(request, 'login.html')


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, _('You are logged out'))
    return redirect('home')
