from django.urls import path

from .views import InvoiceListView, PayInvoiceView

urlpatterns = [
    path("my_invoices/", InvoiceListView.as_view()),
    path("<int:invoice_id>/payment", PayInvoiceView.as_view()),
]
