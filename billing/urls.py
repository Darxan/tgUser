from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path('api', views.PaycomView.as_view(), name="paycom"),
    path('invoice/api', views.InvoiceView.as_view(), name="paycom_invoice"),
    path('transaction/history', views.TransactionHistoryListView.as_view(), name="transaction_history")
]