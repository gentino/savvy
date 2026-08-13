from django.shortcuts import render

# Create your views here.

from groups.models import Group
from withdrawals.models import BankInfo

# Create your views here.
def dashboard(request):
    bankinfo=BankInfo.objects.filter(user=request.user).first()

    wallet = request.user.wallet

    group_count = Group.objects.filter(
        members=request.user
    ).count()

    context = {
        "wallet": wallet,
        "group_count": group_count,
        'bankinfo':bankinfo
    }
    return render(request,'group/dashboard.html',context)

