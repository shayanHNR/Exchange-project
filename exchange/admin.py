from django.contrib import admin
from .models import Customer, Currency, Transaction, Receipt, Custody, Wallet, WalletBalance, AccountLedger

admin.site.register(Customer)
admin.site.register(Currency)
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'transaction_type',
        'from_currency',
        'to_currency',
        'amount',
        'from_wallet',
        'to_wallet',
        'created_at',
    )
admin.site.register(Receipt)
admin.site.register(Custody)
admin.site.register(Wallet)
admin.site.register(WalletBalance)
admin.site.register(AccountLedger)