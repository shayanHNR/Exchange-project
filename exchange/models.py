from django.db import models

class Customer(models.Model):
    name = models.CharField(
        "نام مشتری",
        max_length=100
    )

    phone = models.CharField(
        "شماره تماس",
        max_length=20,
        blank=True
    )

    description = models.TextField(
        "توضیحات",
        blank=True
    )

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"

    def __str__(self):
        return self.name
    def get_balance(self):
        from django.db.models import Sum
        from .models import AccountLedger

        balances = {}

        ledgers = AccountLedger.objects.filter(customer=self)

        for ledger in ledgers:
            key = ledger.currency.code

            if key not in balances:
                balances[key] = 0

            if ledger.entry_type == "CREDIT":
                balances[key] += ledger.amount
            else:
                balances[key] -= ledger.amount

        return balances

class Currency(models.Model):
    name = models.CharField(
        "نام ارز",
        max_length=50
    )

    code = models.CharField(
        "کد ارز",
        max_length=10
    )

    class Meta:
        verbose_name = "ارز"
        verbose_name_plural = "ارزها"

    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('BUY', 'خرید'),
        ('SELL', 'فروش'),
        ('EXCHANGE', 'چنج'),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='مشتری'
    )
    from_wallet = models.ForeignKey(
        'Wallet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='outgoing_transactions',
        verbose_name='کیف پول مبدا'
    )

    to_wallet = models.ForeignKey(
        'Wallet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incoming_transactions',
        verbose_name='کیف پول مقصد'
    )

    transaction_type = models.CharField(
        'نوع معامله',
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    from_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='from_transactions',
        verbose_name='ارز مبدا'
    )

    to_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='to_transactions',
        verbose_name='ارز مقصد'
    )

    amount = models.DecimalField(
        'مبلغ مبدا',
        max_digits=15,
        decimal_places=2
    )

    destination_amount = models.DecimalField(
        "مبلغ مقصد",
        max_digits=20,
        decimal_places=2
    )

    rate = models.DecimalField(
        'نرخ',
        max_digits=15,
        decimal_places=2
    )

    tracking_number = models.CharField(
        'شماره معامله',
        max_length=100,
        unique=True
    )

    note = models.TextField(
        'توضیحات',
        blank=True
    )

    created_at = models.DateTimeField(
        'تاریخ ثبت',
        auto_now_add=True
    )
    class Meta:
        verbose_name = "معامله"
        verbose_name_plural = "معاملات" 
    def __str__(self):
        return f"{self.customer} - {self.transaction_type}"
    
class Receipt(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='receipts',
        verbose_name='معامله'
    )

    file = models.FileField(
        'فایل رسید',
        upload_to='receipts/'
    )
    description = models.TextField(
        'توضیحات',
        blank=True
    )
    created_at = models.DateTimeField(
        'تاریخ ثبت',
        auto_now_add=True
    )
    class Meta:
        verbose_name = "رسید"
        verbose_name_plural = "رسیدها"

    def __str__(self):
        return f"رسید {self.transaction}"
class Custody(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='مشتری'
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        verbose_name='ارز'
    )
    amount = models.DecimalField(
        'مقدار',
        max_digits=15,
        decimal_places=2
    )
    description = models.TextField(
        'توضیحات',
        blank=True
    )
    created_at = models.DateTimeField(
        'تاریخ ثبت',
        auto_now_add=True
    )
    class Meta:
        verbose_name = "امانت"
        verbose_name_plural = "امانت‌ها"

    def __str__(self):
        return f"{self.customer} - {self.amount}"
class Wallet(models.Model):
    name = models.CharField('نام کیف پول',max_length=100)

    description = models.TextField(
        'توضیحات',
        blank=True
    )
    created_at = models.DateTimeField(
        'تاریخ ثبت',
        auto_now_add=True
    )
    class Meta:
        verbose_name = "کیف پول"
        verbose_name_plural = "کیف پول‌ها"

    def __str__(self):
        return self.name
class WalletBalance(models.Model):
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        verbose_name='کیف پول'
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        verbose_name='ارز'
    )
    amount = models.DecimalField(
        'موجودی',
        max_digits=20,
        decimal_places=2,
        default=0
    )
    class Meta:
        verbose_name = "موجودی کیف پول"
        verbose_name_plural = "موجودی کیف پول‌ها"

    def __str__(self):
        return f"{self.wallet} - {self.currency}"
class AccountLedger(models.Model):
    ENTRY_TYPES = (
        ('DEBIT', 'بدهکار'),
        ('CREDIT', 'بستانکار'),
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        null=True,  
        blank=True,
        verbose_name="معامله"
    )
    entry_type = models.CharField(
        "نوع گردش",
        max_length=10,
        choices=ENTRY_TYPES
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='مشتری'
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        verbose_name='ارز'
    )

    amount = models.DecimalField(
        'مبلغ',
        max_digits=20,
        decimal_places=2
    )

    description = models.TextField(
        'توضیحات',
        blank=True
    )

    created_at = models.DateTimeField(
        'تاریخ ثبت',
        auto_now_add=True
    )

    class Meta:
        verbose_name = "گردش حساب"
        verbose_name_plural = "گردش حساب‌ها"

    def __str__(self):
        return f"{self.customer} - {self.amount}"

class CustomerBankAccount(models.Model):

    COUNTRIES = (
        ('IR', 'ایران'),
        ('TR', 'ترکیه'),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="مشتری"
    )

    bank_name = models.CharField(
        "نام بانک",
        max_length=100
    )

    card_number = models.CharField(
        "شماره کارت",
        max_length=30,
        blank=True
    )

    account_number = models.CharField(
        "شماره حساب",
        max_length=50,
        blank=True
    )

    iban = models.CharField(
        "شماره شبا",
        max_length=50,
        blank=True
    )

    country = models.CharField(
        "کشور",
        max_length=2,
        choices=COUNTRIES
    )

    created_at = models.DateTimeField(
        "تاریخ ثبت",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "حساب بانکی مشتری"
        verbose_name_plural = "حساب‌های بانکی مشتریان"

    def __str__(self):
        return f"{self.customer} - {self.bank_name}"
    