from django.urls import path
from .import views 

urlpatterns = [
    
    path('',views.withdrawals,name="withdrawals"),
    path('add_bank',views.add_bank,name="add_bank"),
    path('edit_bank',views.edit_bank,name="edit_bank"),
]
