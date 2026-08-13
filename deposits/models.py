import uuid

from django.conf import settings
from django.db import models


class Deposit(models.Model):

    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"
  

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (SUCCESSFUL, "Successful"),
        (FAILED, "Failed"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="deposits")
    reference = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    amount = models.DecimalField(max_digits=14,decimal_places=2)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=PENDING)

    transaction_reference = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
    

    def save(self, *args, **kwargs):

        if not self.transaction_reference:
            self.transaction_reference = (f"DEP-{uuid.uuid4().hex[:12].upper()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_reference} - ₦{self.amount}"