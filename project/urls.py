from django.urls import path
from . import views
from .views import (
    FraudReportCreateView,
    FraudReportUpdateView,
    TransactionFlagView,
    toggle_transaction_flag
)

urlpatterns = [
    path('stores/', views.StoreListView.as_view(), name='store-list'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('report/<int:pk>/', views.FraudReportDetailView.as_view(), name='fraud-detail'),
    path('report/create/', FraudReportCreateView.as_view(), name='fraud-create'),
    path('report/<int:pk>/edit/', FraudReportUpdateView.as_view(), name='fraud-edit'),
    path('transaction/<int:pk>/flag/', TransactionFlagView.as_view(), name='transaction-flag'),
    path('transaction/<int:pk>/toggle_flag/', toggle_transaction_flag, name='transaction-toggle-flag'),

]

# from .views import TransactionCreateAPI # IS ONLY OCMENT OUT FOR DEPLOY IS OK YES ? 

# urlpatterns += [
#     path('api/transactions/', TransactionCreateAPI.as_view(), name='api-transaction-create'),
# ]

from .views import TransactionGraphView

urlpatterns += [
    path('graphs/transactions/', TransactionGraphView.as_view(), name='transaction-graph'),
]
