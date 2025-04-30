from django.views.generic import ListView, DetailView
from .models import StoreLocation, Transaction, FraudReport

class StoreListView(ListView):
    model = StoreLocation
    template_name = 'stores/store_list.html'

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        qs = Transaction.objects.all().order_by('-date')

        store = self.request.GET.get('store')
        flagged = self.request.GET.get('flagged')
        payment_type = self.request.GET.get('type')

        if store:
            qs = qs.filter(store__id=store)

        if flagged in ['true', 'false']:
            qs = qs.filter(is_flagged=(flagged == 'true'))

        if payment_type:
            qs = qs.filter(payment_type=payment_type)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stores'] = StoreLocation.objects.all()
        context['selected_store'] = self.request.GET.get('store', '')
        context['selected_flagged'] = self.request.GET.get('flagged', '')
        context['selected_type'] = self.request.GET.get('type', '')
        return context


class FraudReportDetailView(DetailView):
    model = FraudReport
    template_name = 'reports/fraud_detail.html'

# project/views.py

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .models import FraudReport, Transaction
from .forms import FraudReportForm, TransactionFlagForm

class FraudReportCreateView(CreateView):
    model = FraudReport
    form_class = FraudReportForm
    template_name = 'reports/fraud_form.html'
    success_url = reverse_lazy('transaction-list')

    def get_initial(self):
        initial = super().get_initial()
        transaction_id = self.request.GET.get('transaction')
        if transaction_id:
            initial['transaction'] = transaction_id
        return initial

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)


class FraudReportUpdateView(UpdateView):
    model = FraudReport
    form_class = FraudReportForm
    template_name = 'reports/fraud_form.html'
    success_url = reverse_lazy('transaction-list')

class TransactionFlagView(UpdateView):
    model = Transaction
    form_class = TransactionFlagForm
    template_name = 'transactions/flag_form.html'
    success_url = reverse_lazy('transaction-list')

# views.py

from django.shortcuts import redirect, get_object_or_404
from .models import Transaction

def toggle_transaction_flag(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.is_flagged = not transaction.is_flagged
    transaction.save()
    return redirect('transaction-list')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TransactionSerializer

VALID_API_KEYS = ['1234', 'abcd', 'deadbeef']  # ✅ Add any keys here

class TransactionCreateAPI(APIView):
    def post(self, request):
        api_key = request.headers.get('X-API-KEY')
        if api_key not in VALID_API_KEYS:
            return Response({'error': 'Invalid or missing API key.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.views.generic import TemplateView
from django.db.models.functions import TruncDay
from django.db.models import Count
from .models import Transaction
import plotly.graph_objs as go
import plotly.offline as opy

class TransactionGraphView(TemplateView):
    template_name = 'graphs/transaction_graph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ===============================
        # Graph 1: Line — Transactions vs Fraud
        # ===============================
        # Total transactions per day
        total = (
            Transaction.objects
            .annotate(day=TruncDay('date'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        # Flagged (fraudulent) transactions per day
        fraud = (
            Transaction.objects
            .filter(is_flagged=True)
            .annotate(day=TruncDay('date'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        # Convert to dicts for easier access
        total_by_day = {entry['day']: entry['count'] for entry in total}
        fraud_by_day = {entry['day']: entry['count'] for entry in fraud}
        all_days = sorted(set(total_by_day) | set(fraud_by_day))

        labels = [day.strftime('%Y-%m-%d') for day in all_days]
        total_counts = [total_by_day.get(day, 0) for day in all_days]
        fraud_counts = [fraud_by_day.get(day, 0) for day in all_days]

        # Plotly traces
        trace_total = go.Scatter(x=labels, y=total_counts, mode='lines+markers', name='All Transactions')
        trace_fraud = go.Scatter(x=labels, y=fraud_counts, mode='lines+markers', name='Flagged (Fraud) Transactions')

        fig1 = go.Figure(data=[trace_total, trace_fraud])
        fig1.update_layout(title='Transactions vs Fraud Over Time', xaxis_title='Date', yaxis_title='Count')
        context['graph1'] = opy.plot(fig1, auto_open=False, output_type='div')

        # ===============================
        # Graph 2: Bar — Payment Types for Fraud
        # ===============================
        fraud_by_type = (
            Transaction.objects
            .filter(is_flagged=True)
            .values('payment_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        payment_labels = [entry['payment_type'].capitalize() for entry in fraud_by_type]
        payment_counts = [entry['count'] for entry in fraud_by_type]

        trace_bar = go.Bar(x=payment_labels, y=payment_counts, name='Fraud by Payment Type')
        fig2 = go.Figure(data=[trace_bar])
        fig2.update_layout(title='Fraudulent Transactions by Payment Type', xaxis_title='Payment Type', yaxis_title='Count')
        context['graph2'] = opy.plot(fig2, auto_open=False, output_type='div')

        return context
