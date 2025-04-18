from django.views.generic import ListView, DetailView
from .models import StoreLocation, Transaction, FraudReport

class StoreListView(ListView):
    model = StoreLocation
    template_name = 'stores/store_list.html'

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'

class FraudReportDetailView(DetailView):
    model = FraudReport
    template_name = 'reports/fraud_detail.html'
