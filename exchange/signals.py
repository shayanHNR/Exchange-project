from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Transaction, WalletBalance
from django.db.models.signals import post_save, post_delete
from .models import (
    Transaction,
    WalletBalance,
    AccountLedger,
)

@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.from_wallet:
        balance, created = WalletBalance.objects.get_or_create(
            wallet=instance.from_wallet,
            currency=instance.from_currency,
            defaults={'amount': 0}
        )

        balance.amount -= instance.amount
        balance.save()

    if instance.to_wallet:
        balance, created = WalletBalance.objects.get_or_create(
            wallet=instance.to_wallet,
            currency=instance.to_currency,
            defaults={'amount': 0}
        )

        balance.amount += instance.destination_amount
        balance.save()
    AccountLedger.objects.create(
        transaction=instance,
        customer=instance.customer,
        currency=instance.from_currency,
        amount=instance.amount,
        entry_type='CREDIT',
        description=f'معامله {instance.tracking_number}'
    )

    AccountLedger.objects.create(
        transaction=instance,
        customer=instance.customer,
        currency=instance.to_currency,
        amount=instance.destination_amount,
        entry_type='DEBIT',
        description=f'معامله {instance.tracking_number}')
@receiver(post_delete, sender=Transaction)
def restore_wallet_balance(sender, instance, **kwargs):
    if instance.from_wallet:
        balance, created = WalletBalance.objects.get_or_create(
            wallet=instance.from_wallet,
            currency=instance.from_currency,
            defaults={'amount': 0})
        balance.amount += instance.amount
        balance.save()
    if instance.to_wallet:
        balance, created = WalletBalance.objects.get_or_create(
            wallet=instance.to_wallet,
            currency=instance.to_currency,
            defaults={'amount': 0})
        balance.amount -= instance.destination_amount
        balance.save()
  