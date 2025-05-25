from django.contrib import admin

from invoice.models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_filter = ("status",)
    search_fields = (
        "subscription__user__email",
        "subscription__user__first_name",
        "subscription__user__last_name",
    )
    list_display = ("id", "subscription", "status", "amount", "created_at", "updated_at")
    list_display_links = ("id", "subscription")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("subscription", "status", "amount")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
