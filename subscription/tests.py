from django.test import TestCase
from datetime import datetime, timedelta
from user.models import User
from subscription.models import Subscription, Plans, SubscriptionStatus


class SubscriptionModelTestCase(TestCase):
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
            status=SubscriptionStatus.ACTIVE,
        )

    def test_subscription_creation(self):
        """Test that a subscription is created successfully."""
        self.assertEqual(self.subscription.user, self.user)
        self.assertEqual(self.subscription.plan, self.plan)
        self.assertEqual(self.subscription.status, SubscriptionStatus.ACTIVE)

    def test_subscription_string_representation(self):
        """Test the string representation of the subscription."""
        expected_str = f"{self.user.first_name} {self.user.last_name}    {self.plan.name}    {self.subscription.status}"
        self.assertIn(expected_str, str(self.subscription))

    def test_subscription_expiry(self):
        """Test that a subscription is marked as expired after the end date."""
        self.subscription.end_date = datetime.now().date() - timedelta(days=1)
        self.subscription.status = SubscriptionStatus.EXPIRED
        self.subscription.save()
        self.assertEqual(self.subscription.status, SubscriptionStatus.EXPIRED)

    def test_subscription_cancellation(self):
        """Test that a subscription can be canceled."""
        self.subscription.status = SubscriptionStatus.CANCELLED
        self.subscription.is_active = False
        self.subscription.save()
        self.assertEqual(self.subscription.status, SubscriptionStatus.CANCELLED)
        self.assertFalse(self.subscription.is_active)
