from django.contrib import admin
from .models import Withdrawal, BankInfo

#Register your models here.
# =========================================================
# WITHDRAWAL ADMIN
# =========================================================

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
        "updated_at",
    )

    search_fields = (
        "user__email",
        "user__username",
    )

    ordering = ("-updated_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Withdrawal Information",
            {
                "fields": (
                    "user",
                    "amount",
                    "status",
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
# BANK INFO ADMIN
# =========================================================

@admin.register(BankInfo)
class BankInfoAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "bank_name",
        "account_name",
        "account_number",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "bank_name",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__username",
        "bank_name",
        "account_name",
        "account_number",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Bank Account Information",
            {
                "fields": (
                    "user",
                    "bank_name",
                    "account_name",
                    "account_number",
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
