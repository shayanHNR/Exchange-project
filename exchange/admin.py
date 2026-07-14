from django.contrib import admin
from .models import Customer, Currency, Transaction, Receipt, Custody, Wallet, WalletBalance, AccountLedger, CustomerBankAccount

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
        'destination_amount',
        'from_wallet',
        'to_wallet',
        'created_at',
    )
admin.site.register(Receipt)
admin.site.register(Custody)
admin.site.register(Wallet)
admin.site.register(WalletBalance)
@admin.register(AccountLedger)
class AccountLedgerAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'currency',
        'amount',
        'entry_type',
        'created_at',
    )
admin.site.register(CustomerBankAccount)