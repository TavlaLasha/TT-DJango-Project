from django.contrib import admin

from .models import Customers, Orders

admin.site.register(Customers)

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('orderid','cutomerid', 'statusid', 'statusdate', 'orderdate')
    # search_fields = ['cutomerid']


admin.site.register(Orders, OrdersAdmin)

