from subscription.models import Subscription, SubscriptionStatus
from .models import Invoice, InvoiceStatus
from celery import shared_task
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task(name="generate_invoices", queue="main_queue")
def generate_invoices():
    logger.info("Invoice generation task:processing")

    today = datetime.now().date()
    subscriptions = Subscription.objects.filter(start_date=today, status=SubscriptionStatus.ACTIVE)

    for subscription in subscriptions:
        invoice_instance = Invoice.objects.create(
            subscription=subscription,
            amount=subscription.plan.price,
            issue_date=today,
            due_date=today + timedelta(days=30),
        )
        logger.debug(
            f"Invoice created for subscription {subscription.id} with amount {invoice_instance.amount}."
        )
    logger.info(f"Total invoices generated: {subscriptions.count()}")
    logger.info("Invoice generation task:completed")


@shared_task(name="mark_overdue_unpaid_invoice", queue="main_queue")
def mark_overdue_unpaid_invoice():
    logger.info("Mark unpaid invoices task:processing.")
    Invoice.objects.filter(
        due_date__lt=datetime.now(),
        subscription__is_active=True,
        overdue=False,
        status=InvoiceStatus.PENDING,
    ).update(overdue=True)
    logger.info("Mark unpaid invoices task:completed.")


@shared_task(name="send_reminder_email", queue="main_queue")
def send_reminder_email():
    logger.debug("Sending reminder emails for overdue invoices.")
    Invoices = Invoice.objects.filter(
        overdue=False, status=InvoiceStatus.PENDING, subscription__is_active=True
    )
    for invoice in Invoices:
        logger.debug(
            f"Sending reminder email to {invoice.subscription.user.email} for invoice={invoice.id} is pending, Due date is {invoice.due_date}."
        )

    logger.info(f"")
