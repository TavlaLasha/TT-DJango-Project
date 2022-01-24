import datetime
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm, PasswordResetFrom
from .models import Orders, Cities, Customers, PaymentType, Status, Orderdetails, Product, Category
from pprint import pprint
import time

# For Password Reset
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.views.generic import ListView
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


def password_reset(request):
    if request.method == "POST":
        form = PasswordResetFrom(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            associated_users = Customers.objects.filter(Q(email=email))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "auth/passReset/pass_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Tech Trade Store',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'support@TTStore.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    else:
        form = PasswordResetFrom()
    return render(request, 'auth/passReset/password_reset.html', {'form': form})


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
        'mostSold': get_product_sales_statistics('mostSold', True),
        'leastSold': get_product_sales_statistics('leastSold', True),
        'popularCategories': get_most_popular_categories(),
    }

    return render(request, 'statistics/index.html', data)

def get_recent_sales():
    data = []
    time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(days=10)
    orderList = Orders.objects.filter(orderdate__gt=time_threshold)

    if orderList.count() != 0:
        for order in orderList:
            priceSum = 0

            fullOrderData = order
            fullOrderData.payment = order.paymenttype.payment
            fullOrderData.customerName = order.cutomerid.username
            fullOrderData.status = order.statusid.status

            # 1 to many relationshipis gamo OrderDetails shi, sheidzleba ramdenime produqti iyos ert orderze
            items = Orderdetails.objects.filter(orderid=order.orderid)

            for item in items:
                priceSum += item.total

            fullOrderData.total_price = priceSum

            data.append(fullOrderData)

    return data


def get_sales_sum():
    orderList = Orderdetails.objects.filter()
    lifetimeSales = 0

    for order in orderList:
        lifetimeSales += order.total

    return lifetimeSales


def get_new_customers():
    time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(days=10)

    return Customers.objects.filter(date_joined__gt=time_threshold)


def get_product_sales_statistics(orderType, limit=False):
    order = "salesCount"
    itemList = []

    if orderType == "mostSold":
        order = "-salesCount"

    sortedItems = Orderdetails.objects.filter().values("productid").annotate(salesCount=Sum("quantity")).order_by(order)

    if limit:
        sortedItems = sortedItems[:10]

    for item in sortedItems:
        itemData = item
        itemData["product"] = Product.objects.get(productid=item["productid"])

        itemList.append(itemData)

    return itemList


def get_most_popular_categories():
    itemSales = get_product_sales_statistics("mostSold")
    salesLib = []
    sortedData = []
    salesPerCategory = {}

    for item in itemSales:
        libData = item
        libData['category_id'] = item["product"].categoryid.categoryid
        libData['category_name'] = Category.objects.get(categoryid=item["product"].categoryid.categoryid).categoryname

        salesLib.append(libData)

    for sale in salesLib:
        if sale['category_id'] in salesPerCategory:
            salesPerCategory[sale['category_id']['count']] += sale['salesCount']
        else:
            salesPerCategory[sale['category_id']] = {
                'count': sale['salesCount'],
                'name': sale['category_name'],
            }

    for sale in salesPerCategory.values():
        sortedData.append(sale)

    return sortedData

def get_orders_by_account(request):
    results = Orders.objects.filter(cutomerid=5)

    return render(request, 'OrdersView.html', {'results': results})

class orderlist(ListView):
    orders = Orders.objects.filter(cutomerid=5)