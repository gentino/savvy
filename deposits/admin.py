from django.contrib import admin
from django.contrib import messages
from .models import Deposit
from wallet.services import approve_deposit


@admin.action(description="Approve selected deposits")
def approve_selected_deposits(modeladmin, request, queryset):

    for deposit in queryset:

        success, message = approve_deposit(deposit)

        if success:
            modeladmin.message_user(
                request,
                f"{deposit.transaction_reference}: {message}",
                messages.SUCCESS
            )
        else:
            modeladmin.message_user(
                request,
                f"{deposit.transaction_reference}: {message}",
                messages.ERROR
            )

@admin.action(description="Reject selected deposits")
def reject_selected_deposits(modeladmin, request, queryset):

    for deposit in queryset:

        success, message = reject_deposit(deposit)

        if success:
            modeladmin.message_user(
                request,
                f"{deposit.transaction_reference}: {message}",
                messages.SUCCESS
            )
        else:
            modeladmin.message_user(
                request,
                f"{deposit.transaction_reference}: {message}",
                messages.ERROR
            )


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):

    list_display = (
        "transaction_reference",
        "user",
        "amount",
        "status",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "transaction_reference",
        "user__email",
        "user__username",
    )

    actions = [
        approve_selected_deposits,
        reject_selected_deposits,
    ]
    
    
