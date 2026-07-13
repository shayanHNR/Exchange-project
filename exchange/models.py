from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

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

    def __str__(self):
        return f"{self.customer} - {self.transaction_type}"