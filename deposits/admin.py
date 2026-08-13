from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Deposit


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__username",
    )

    ordering = ("-created_at",)

    readonly_fields = ("created_at",)

    fieldsets = (
        (
            "Deposit Information",
            {
                "fields": (
                    "user",
                    "amount",
                    "status",
                )
            },
        ),
        ("Date Information", {"fields": ("created_at",)}),
    )


# Register your models here.
