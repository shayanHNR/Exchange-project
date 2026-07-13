from django.contrib import admin
from .models import Customer, Currency, Transaction, Receipt, Custody, Wallet, WalletBalance, AccountLedger

admin.site.register(Customer)
admin.site.register(Currency)
admin.site.register(Transaction)
admin.site.register(Receipt)
admin.site.register(Custody)
admin.site.register(Wallet)
admin.site.register(WalletBalance)
admin.site.register(AccountLedger)