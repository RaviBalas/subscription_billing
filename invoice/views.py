from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.custom_pagination import CustomPagination
from invoice.serializers import InvoiceSerializer
from .models import Invoice, InvoiceStatus


class InvoiceListView(generics.ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        output = {"data": {}, "type": "success", "message": None}
        status_code = status.HTTP_200_OK
        plans = self.get_queryset().filter(
            subscription__user=request.user, subscription__is_active=True
        )
        page = self.paginate_queryset(plans)
        if page is not None:
            serialized_data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(serialized_data)
        output["data"] = self.get_serializer(plans, many=True).data
        return Response(output, status=status_code)


class PayInvoiceView(APIView):

    def post(self, request, invoice_id, *args, **kwargs):
        output = {"data": {}, "type": "success", "message": None}
        status_code = status.HTTP_200_OK
        try:
            invoice = Invoice.objects.get(id=invoice_id, subscription__user=request.user)
            if invoice.status == InvoiceStatus.PAID:
                output["type"] = "error"
                output["message"] = "This invoice has already been paid."
                return Response(output, status=status.HTTP_400_BAD_REQUEST)
            invoice.status = InvoiceStatus.PAID
            invoice.save()
            output["message"] = "Invoice payment successful."
        except Invoice.DoesNotExist:
            output["type"] = "error"
            output["message"] = "Invoice not found."
        return Response(output, status=status_code)
