from django.contrib import admin

from .models import Plans, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "start_date", "end_date", "status")
    search_fields = ("user__email", "plan__name")
    list_filter = ("status", "plan")
    ordering = ("-start_date",)


@admin.register(Plans)
class PlansAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)
