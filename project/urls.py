from django.urls import path
from . import views

urlpatterns = [
    path('stores/', views.StoreListView.as_view(), name='store-list'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('report/<int:pk>/', views.FraudReportDetailView.as_view(), name='fraud-detail'),
]
