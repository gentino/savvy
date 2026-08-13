from django.urls import path
from .import views 

urlpatterns = [
    
    path('',views.withdrawals,name="withdrawals"),
    path('confirm',views.confirm,name="confirm_withdrawal"),
    path('reject',views.reject,name="reject_withdrawal"),
    path('add_bank',views.add_bank,name="add_bank"),
    path('edit_bank',views.edit_bank,name="edit_bank"),
]