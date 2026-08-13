from django.db import models
from django.conf import settings
from groups.models import Group



class Notification(models.Model):

    # Group-related notifications
    JOIN_REQUEST = "join_request"
    JOIN_APPROVED = "join_approved"
    JOIN_REJECTED = "join_rejected"
    MEMBER_JOINED = "member_joined"

    # Wallet-related notifications
    DEPOSIT = "deposit"
    DEPOSIT_APPROVED = "deposit_approved"
    DEPOSIT_REJECTED = "deposit_rejected"

    WITHDRAWAL = "withdrawal"
    WITHDRAWAL_APPROVED = "withdrawal_approved"
    WITHDRAWAL_REJECTED = "withdrawal_rejected"

    # Savings / contribution
    CONTRIBUTION = "contribution"

    OTHER = "other"

    NOTIFICATION_TYPES = (
        (JOIN_REQUEST, "Join Request"),
        (JOIN_APPROVED, "Join Approved"),
        (JOIN_REJECTED, "Join Rejected"),
        (MEMBER_JOINED, "Member Joined"),

        (DEPOSIT, "Deposit"),
        (DEPOSIT_APPROVED, "Deposit Approved"),
        (DEPOSIT_REJECTED, "Deposit Rejected"),

        (WITHDRAWAL, "Withdrawal"),
        (WITHDRAWAL_APPROVED, "Withdrawal Approved"),
        (WITHDRAWAL_REJECTED, "Withdrawal Rejected"),
        (CONTRIBUTION, "Contribution"),

        (OTHER, "Other"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="notifications")
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name="notifications",null=True,blank=True)
    type = models.CharField(max_length=30,choices=NOTIFICATION_TYPES)
    amount = models.DecimalField(max_digits=14,decimal_places=2,null=True,blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def message(self):
        group_name = self.group.name if self.group else "your group"
        amount = f"₦{self.amount:,.2f}" if self.amount is not None else ""
        messages = {
            self.JOIN_REQUEST:
                f"Someone requested to join {group_name}.",
            self.JOIN_APPROVED:
                f"Your request to join {group_name} was approved.",

            self.JOIN_REJECTED:
                f"Your request to join {group_name} was rejected.",

            self.MEMBER_JOINED:
                f"A new member joined {group_name}.",

            self.DEPOSIT:
                f"Your deposit request of {amount} has been submitted and is awaiting approval.",

            self.DEPOSIT_APPROVED:
                f"Your deposit of {amount} has been approved and your wallet has been credited.",

            self.DEPOSIT_REJECTED:
                f"Your deposit request of {amount} has been rejected.",

            self.WITHDRAWAL:
                f"Your withdrawal request of {amount} has been submitted.",

            self.WITHDRAWAL_APPROVED:
                f"Your withdrawal of {amount} has been approved.",

            self.WITHDRAWAL_REJECTED:
                f"Your withdrawal request of {amount} has been rejected.",

            self.CONTRIBUTION:
                f"A contribution of {amount} was made to {group_name}.",
            
            self.OTHER:
                "You have a new notification.",
        }

        return messages.get(
            self.type,
            "You have a new notification."
        )