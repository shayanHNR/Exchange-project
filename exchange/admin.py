from django.contrib import admin
from .models import Customer, Currency, Transaction, Receipt, Custody, Wallet, WalletBalance, AccountLedger, CustomerBankAccount

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'balance',
    )

    def balance(self, obj):
        data = obj.get_balance()
        return " | ".join(
            [f"{key}: {value}" for key, value in data.items()]
        )

    balance.short_description = "مانده حساب"
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
        'signed_amount',
    )
    def signed_amount(self, obj):
        if obj.entry_type == "CREDIT":
            return obj.amount

        return -obj.amount

    signed_amount.short_description = "مبلغ با علامت"
admin.site.register(CustomerBankAccount)