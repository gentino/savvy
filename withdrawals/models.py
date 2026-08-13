from django.db import models
from django.conf import settings 
# Create your models here.

class Withdrawal(models.Model):
    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"
      
    
    STATUS_CHOICES = (
            (PENDING, "Pending"),
            (SUCCESSFUL, "Successful"),
            (FAILED, "Failed"),
        )
        
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="withdrawals")
    amount = models.DecimalField(max_digits=12,decimal_places=2, null=False)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default=PENDING)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-updated_at"]
    
    
    def __str__(self):
        return f'{self.user} -  {self.amount} - {self.status}'
    
    

class BankInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=20, null=False, blank=False)
    account_number = models.CharField(max_length=10, null=False)
    account_name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.bank_name} - {self.account_number}"
        
    
    