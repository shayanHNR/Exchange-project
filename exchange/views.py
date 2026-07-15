from django.shortcuts import render

from .models import Customer


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
