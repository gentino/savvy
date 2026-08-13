from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request,'index.html')

def privacy(request):
    return render(request,'privacy.html')



def security(request):
    return render(request,'security.html')

def terms_and_conditions(request):
    return render(request,'terms_and_conditions.html')

def Contact_us(request):
    return render(request,'Contact_us.html')
