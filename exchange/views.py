from django.shortcuts import render
from django.core.paginator import Paginator
from .models import (Customer,
                     Transaction,
                     Wallet,
                     Currency,
                     WalletBalance,
)
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
def dashboard(request):

    customer_count = Customer.objects.count()

    transaction_count = Transaction.objects.count()

    wallet_count = Wallet.objects.count()

    currency_count = Currency.objects.count()

    return render(
        request,
        'exchange/dashboard.html',
        {
            'customer_count': customer_count,
            'transaction_count': transaction_count,
            'wallet_count': wallet_count,
            'currency_count': currency_count,
        }
    )
def transaction_list(request):

    search = request.GET.get('search')

    transactions = Transaction.objects.all()

    if search:
        transactions = transactions.filter(
            customer__name__icontains=search
        )

    transactions = transactions.order_by(
        '-created_at'
    )
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)

    return render(
        request,
        'exchange/transaction_list.html',
        {
            'transactions': transactions,
            'search': search,
        }
    )
def customer_list(request):

    search = request.GET.get('search')

    customers = Customer.objects.all()

    if search:
        customers = customers.filter(
            name__icontains=search
        )

    customers = customers.order_by('name')

    return render(
        request,
        'exchange/customer_list.html',
        {
            'customers': customers,
            'search': search,
        }
    )