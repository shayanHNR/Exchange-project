from django.shortcuts import render

from .models import Customer,Transaction


def customer_report(request, customer_id):
    customer = Customer.objects.get(id=customer_id)

    balance = customer.get_balance()
    transactions = customer.transaction_set.all().order_by('-created_at')

    return render(
        request,
        'exchange/customer_report.html',
        {
            'customer': customer,
            'balance': balance,
            'transactions': transactions,
        }
    )
def transaction_invoice(request, transaction_id):
    transaction = Transaction.objects.get(
        id=transaction_id
    )
    return render(
        request,
        'exchange/transaction_invoice.html',
        {
            'transaction': transaction,
        }
    )
from .models import WalletBalance

def wallet_report(request):
    balances = WalletBalance.objects.all().order_by(
        'wallet','currency'
    )
    return render(
        request,
        'exchange/wallet_report.html',
        {
            'balances': balances,
        }
    )