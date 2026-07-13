from django.contrib import admin
from .models import Customer, Currency, Transaction, Receipt

admin.site.register(Customer)
admin.site.register(Currency)
admin.site.register(Transaction)
admin.site.register(Receipt)