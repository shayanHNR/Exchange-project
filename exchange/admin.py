from django.contrib import admin
from .models import Customer, Currency, Transaction, Receipt, Custody

admin.site.register(Customer)
admin.site.register(Currency)
admin.site.register(Transaction)
admin.site.register(Receipt)
admin.site.register(Custody)