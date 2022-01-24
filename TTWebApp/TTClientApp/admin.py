from atexit import register
from django.contrib import admin

# from .models import Customers, AbstractBaseUser
from .models import Customers
admin.site.register(Customers)
# admin.site.register(AbstractBaseUser)

  