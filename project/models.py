from django.db import models
from django.contrib.auth.models import User

class StoreLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"

class Transaction(models.Model):
    store = models.ForeignKey(StoreLocation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50, choices=[
        ('credit', 'Credit Card'),
        ('cash', 'Cash'),
        ('gift', 'Gift Card'),
        ('online', 'Online Payment'),
    ])
    date = models.DateField()
    location_description = models.CharField(max_length=200)
    is_flagged = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.store.name} - ${self.amount} on {self.date}"

class FraudReport(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('new', 'New'),
        ('review', 'Under Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ], default='new')

    def __str__(self):
        return f"Report on {self.transaction} by {self.reporter.username}"
