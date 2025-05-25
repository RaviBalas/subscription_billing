from django.db import models
from common.audit import Audit
from user.models import User


class SubscriptionStatus(models.TextChoices):
    ACTIVE = "Active"
    CANCELLED = "Cancelled"
    EXPIRED = "Expired"


class Plans(Audit):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"

    def __str__(self):
        return self.name


class Subscription(Audit):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="my_subscriptions",
        related_query_name="subscription",
    )
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE, related_name="my_plans")
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=SubscriptionStatus,
        default=SubscriptionStatus.ACTIVE,
    )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return "    ".join(
            (
                self.user.first_name + " " + self.user.last_name,
                self.plan.name,
                self.status,
                str((self.end_date - self.start_date).days),
                "days",
                self.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                self.end_date.strftime("%Y-%m-%d %H:%M:%S"),
            )
        )
