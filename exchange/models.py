from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"

    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
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
        on_delete=models.CASCADE
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    from_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='from_transactions'
    )

    to_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name='to_transactions'
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    rate = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    tracking_number = models.CharField(
        max_length=100,
        unique=True
    )

    note = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
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
        related_name='receipts'
    )

    file = models.FileField(
        upload_to='receipts/'
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
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
        on_delete=models.CASCADE
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "امانت"
        verbose_name_plural = "امانت‌ها"

    def __str__(self):
        return f"{self.customer} - {self.amount}"
class Wallet(models.Model):
    name = models.CharField(max_length=100)

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
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
        on_delete=models.CASCADE
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
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
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "گردش حساب"
        verbose_name_plural = "گردش حساب‌ها"

    def __str__(self):
        return f"{self.customer} - {self.amount}"