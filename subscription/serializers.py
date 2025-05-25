from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Subscription, Plans


class SubscribeSerializer(serializers.ModelSerializer):
    """
    Serializer for  subscription of plan.

    """

    plan = serializers.PrimaryKeyRelatedField(
        queryset=Plans.objects.all(),
        error_messages={"does_not_exist": "The selected plan does not exist."},
    )

    class Meta:
        model = Subscription
        fields = ["plan", "user", "start_date", "end_date"]

    def validate(self, data):
        """
        Validate the subscription data.

        Ensures that the plan is valid and that the user is not already subscribed.
        """
        if data["start_date"] >= data["end_date"]:
            raise serializers.ValidationError(
                {"end_date": ["end_date must be greater than start_date."]}
            )
        if Subscription.objects.filter(user=data["user"], is_active=True).exists():
            raise serializers.ValidationError(
                {"plan": ["You already have an active subscription."]}
            )
        return data

    def create(self, validated_data):
        """
        Create a new user instance with the validated data.
        """
        return self.Meta.model.objects.create(**validated_data)


class UnSubscribeSerializer(serializers.ModelSerializer):
    """
    serializer for unsubscribing from a plan.
    This serializer is used to handle the unscribing process for a user from a specific plan.
    """

    plan = serializers.PrimaryKeyRelatedField(
        queryset=Plans.objects.all(),
        error_messages={"does_not_exist": "The selected plan does not exist."},
    )

    class Meta:
        model = Subscription
        fields = ["plan", "user", "start_date", "end_date"]

    def validate(self, data):
        """
        Validate the subscription data.
        Ensures that the plan is valid and that the user is subscribed to the plan they are trying to unsubscribe from.
        """
        if not Subscription.objects.filter(
            user=data["user"], plan=data["plan"], is_active=True
        ).exists():
            raise serializers.ValidationError({"plan": ["You don't have any active subscription."]})
        return data


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = ["id", "name", "price"]


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    plan = PlanSerializer()

    class Meta:
        model = Subscription
        fields = "__all__"
        depth = 1
