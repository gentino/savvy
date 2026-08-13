from django.contrib import admin
from .models import Wallet, WalletTransaction, GroupSavings


# =========================================================
# WALLET ADMIN
# =========================================================

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "balance",
        "reserved_balance",
        "total_deposited",
        "total_withdrawn",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__email",
        "user__username",
        "user__first_name",
        "user__last_name",
    )

    ordering = ("-updated_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Wallet Information",
            {
                "fields": (
                    "user",
                    "balance",
                    "reserved_balance",
                )
            },
        ),

        (
            "Wallet Statistics",
            {
                "fields": (
                    "total_deposited",
                    "total_withdrawn",
                )
            },
        ),

        (
            "Date Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


# =========================================================
# WALLET TRANSACTION ADMIN
# =========================================================

@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "wallet",
        "reference",
        "transaction_type",
        "amount",
        "status",
        "balance_before",
        "balance_after",
        "created_at",
    )

    list_filter = (
        "transaction_type",
        "status",
        "created_at",
    )

    search_fields = (
        "wallet__user__email",
        "wallet__user__username",
        "reference",
        "gateway_reference",
        "description",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "reference",
        "balance_before",
        "balance_after",
        "created_at",
    )

    fieldsets = (
        (
            "Transaction Information",
            {
                "fields": (
                    "wallet",
                    "reference",
                    "transaction_type",
                    "amount",
                    "status",
                )
            },
        ),

        (
            "Balance Information",
            {
                "fields": (
                    "balance_before",
                    "balance_after",
                )
            },
        ),

        (
            "Payment Information",
            {
                "fields": (
                    "gateway_reference",
                    "description",
                )
            },
        ),

        (
            "Date Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )


# =========================================================
# GROUP SAVINGS ADMIN
# =========================================================

@admin.register(GroupSavings)
class GroupSavingsAdmin(admin.ModelAdmin):

    list_display = (
        "group",
        "user",
        "balance",
        "total_contributed",
        "total_withdrawn",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "group",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "group__name",
        "user__email",
        "user__username",
        "user__first_name",
        "user__last_name",
    )

    ordering = ("-updated_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Group Savings",
            {
                "fields": (
                    "group",
                    "user",
                    "balance",
                )
            },
        ),

        (
            "Savings Statistics",
            {
                "fields": (
                    "total_contributed",
                    "total_withdrawn",
                )
            },
        ),

        (
            "Date Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

