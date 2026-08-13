from django.urls import path
from . import views

urlpatterns = [
    path("", views.notifications, name="notifications"),
    path("withdrawals", views.withdrawal_notifications, name="withdrawal_notification"),
    path("deposits", views.deposit_notifications, name="deposit_notification"),
    path("notification/<int:id>", views.read, name="read_notification"),
    path("delete/<int:id>", views.delete, name="delete_notification"),
]
