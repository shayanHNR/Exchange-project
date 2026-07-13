from django.contrib import admin
from .models import Customer, Currency, Transaction

admin.site.register(Customer)
admin.site.register(Currency)
admin.site.register(Transaction)
