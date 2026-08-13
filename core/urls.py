from django.urls import path
from . import views 



urlpatterns = [
    path('',views.home,name="home"),
    path('privacy',views.privacy, name="privacy"),
    path('security',views.security, name="security"),
    path('terms_and_conditions',views.terms_and_conditions, name="terms_of_service"),
    path('contact_us',views.Contact_us, name="Contact_us")
    

]