from rest_framework import serializers

from subscription.serializers import SubscriptionSerializer
from subscription.views import SubscribePlanView
from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()

    class Meta:
        model = Invoice
        fields = ("id", "amount", "issue_date", "due_date", "overdue", "status", "subscription")
