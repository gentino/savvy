from django.urls import path
from .import views


urlpatterns = [
    path('',views.wallet, name="wallet"),
    path('save/<int:id>',views.save,name="save"),
    path("transactions/",views.transactions,name="transactions"),
]
