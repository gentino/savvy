from django.urls import path
from .import views

urlpatterns = [
 path('',views.notifications,name="notifications"), 
 path('notification/<int:id>',views.read,name="read_notification"), 
 path('delete/<int:id>',views.delete,name="delete_notification")
]

