from django.db import models
from common.audit import Audit
from subscription.models import Subscription


class InvoiceStatus(models.TextChoices):
    PENDING = "Pending"
    PAID = "Paid"


class Invoice(Audit):
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="my_invoices",
        related_query_name="SubscriptionInVoice",
    )
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    issue_date = models.DateTimeField()
    due_date = models.DateTimeField()
    overdue = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10, choices=InvoiceStatus.choices, default=InvoiceStatus.PENDING
    )

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        return " | ".join(
            (f"Invoice #{self.id}", str(self.amount), str(self.issue_date), self.status)
        )
