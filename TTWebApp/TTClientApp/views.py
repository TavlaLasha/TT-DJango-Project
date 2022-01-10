import datetime
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from .models import Orders, Cities, Customers, PaymentType, Status
import time


def index(request):
    return render(request, 'index.html')


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'auth/login.html', context)


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'auth/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def statistics_view(request):
    data = {
        'orders': get_recent_sales(),
        'salesSum': get_sales_sum(),
        'newCustomers': get_new_customers(),
    }

    return render(request, 'statistics/index.html', data)

def get_recent_sales():
    data = []
    unixTime = time.time()
    # daabrunebs shekvetebs bolo 10 dgidan {Current unix timestamp - 10 days (864000))
    orderAge = unixTime - 864000
    orderList = Orders.objects.filter(orderdate__gt=orderAge)

    if orderList.count() != 0:
        for order in orderList:
            fullOrderData = order
            fullOrderData.payment = order.paymenttype.payment
            fullOrderData.customerName = order.cutomerid.username
            fullOrderData.status = order.statusid.status

            data.append(fullOrderData)

    return data


def get_sales_sum():
    orderList = Orders.objects.filter()
    lifetimeSales = 0

    for order in orderList:
        lifetimeSales += order.total_price
    return lifetimeSales


def get_new_customers():
    time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(days=100)

    return Customers.objects.filter(date_joined__gt=time_threshold)
