# project/forms.py

from django import forms
from .models import FraudReport, Transaction

class FraudReportForm(forms.ModelForm):
    class Meta:
        model = FraudReport
        fields = ['transaction', 'description', 'status']

class TransactionFlagForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['is_flagged']
