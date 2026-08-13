from django.db import models
from django.conf import settings
import uuid
from groups.models import Group

# Create your models here.
class Wallet(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="wallet")
    balance = models.DecimalField(max_digits=14,decimal_places=2,default=0)
    reserved_balance = models.DecimalField(max_digits=14,decimal_places=2,default=0)
    total_deposited = models.DecimalField(max_digits=14,decimal_places=2,default=0)
    total_withdrawn = models.DecimalField(max_digits=14,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} Wallet"
    
    
class WalletTransaction(models.Model):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    CONTRIBUTION = "contribution"
    REFUND = "refund"
    PENALTY = "penalty"
    ADJUSTMENT = "adjustment"
    
    
    TRANSACTION_TYPES = (
        (DEPOSIT, "Deposit"),
        (WITHDRAWAL, "Withdrawal"),
        (CONTRIBUTION, "Contribution"),
        (REFUND, "Refund"),
        (PENALTY, "Penalty"),
        (ADJUSTMENT, "Adjustment"),
    )

    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    CANCELLED = "cancelled"

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (SUCCESSFUL, "Successful"),
        (FAILED, "Failed"),
        (CANCELLED, "Cancelled"),
        )


    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE,related_name="transactions")
    reference = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    transaction_type = models.CharField(max_length=20,choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=14,decimal_places=2)
    balance_before = models.DecimalField(max_digits=14,decimal_places=2)
    balance_after = models.DecimalField(max_digits=14,decimal_places=2)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=PENDING)
    description = models.CharField(max_length=255,blank=True)
    gateway_reference = models.CharField(max_length=150,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.wallet.user} - {self.amount}"
    
    

class GroupSavings(models.Model):
        
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name="savings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="group_savings")
    balance = models.DecimalField(max_digits=14,decimal_places=2,default=0)
    total_contributed = models.DecimalField(max_digits=14,decimal_places=2,default=0)
    total_withdrawn = models.DecimalField(max_digits=14,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contributed_at = models.DateTimeField(null=True,blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "user"],
                name="unique_user_group_savings"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.group} Savings"
    
    
    