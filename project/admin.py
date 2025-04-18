from django.contrib import admin
from .models import StoreLocation, Transaction, FraudReport

admin.site.register(StoreLocation)
admin.site.register(Transaction)
admin.site.register(FraudReport)
