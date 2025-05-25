from django.test import TestCase
from datetime import datetime, timedelta
from subscription.models import Subscription, Plans, SubscriptionStatus
from invoice.models import Invoice, InvoiceStatus
from user.models import User


class InvoiceModelTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
        )

        # Create a plan
        self.plan = Plans.objects.create(name="Basic", price=100.00)

        # Create a subscription
        self.subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            start_date=datetime.now().date(),
            end_date=(datetime.now() + timedelta(days=30)).date(),
        )

        # Create an invoice
        self.invoice = Invoice.objects.create(
            subscription=self.subscription,
            amount=self.plan.price,
            issue_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=30),
            overdue=False,
            status=InvoiceStatus.PENDING,
        )

    def test_invoice_creation(self):
        """Test that an invoice is created successfully."""
        self.assertEqual(self.invoice.subscription, self.subscription)
        self.assertEqual(self.invoice.amount, self.plan.price)
        self.assertEqual(self.invoice.status, InvoiceStatus.PENDING)

    def test_invoice_string_representation(self):
        """Test the string representation of the invoice."""
        expected_str = f"Invoice #{self.invoice.id} | {self.invoice.amount} | {self.invoice.issue_date} | {self.invoice.status}"
        self.assertEqual(str(self.invoice), expected_str)

    def test_invoice_overdue_status(self):
        """Test that the overdue status is updated correctly."""
        self.invoice.due_date = datetime.now() - timedelta(days=1)
        self.invoice.save()
        self.assertTrue(self.invoice.due_date < datetime.now())
