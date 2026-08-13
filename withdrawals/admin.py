from django.contrib import admin, messages

from .models import Withdrawal
from wallet.services import (
    approve_withdrawal,
    reject_withdrawal,
)


@admin.action(description="Approve selected withdrawals")
def approve_selected_withdrawals(modeladmin, request, queryset):

    for withdrawal in queryset:

        success, message = approve_withdrawal(withdrawal)

        if success:
            modeladmin.message_user(
                request,
                f"₦{withdrawal.amount:,.2f}: {message}",
                messages.SUCCESS
            )
        else:
            modeladmin.message_user(
                request,
                f"₦{withdrawal.amount:,.2f}: {message}",
                messages.ERROR
            )


@admin.action(description="Reject selected withdrawals")
def reject_selected_withdrawals(modeladmin, request, queryset):

    for withdrawal in queryset:

        success, message = reject_withdrawal(withdrawal)

        if success:
            modeladmin.message_user(
                request,
                f"₦{withdrawal.amount:,.2f}: {message}",
                messages.SUCCESS
            )
        else:
            modeladmin.message_user(
                request,
                f"₦{withdrawal.amount:,.2f}: {message}",
                messages.ERROR
            )


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):

    list_display = (
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
        "user__email",
        "user__username",
    )

    actions = [
        approve_selected_withdrawals,
        reject_selected_withdrawals,
    ]