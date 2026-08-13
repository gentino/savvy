from django.shortcuts import render,get_object_or_404
from groups.models import Group
from withdrawals.models import BankInfo
from wallet.models import Wallet


# Create your views here.
def dashboard(request):
    bankinfo=BankInfo.objects.filter(user=request.user).first()
    wallet = request.user.wallet
    group_count = Group.objects.filter(members=request.user).count()
    transactions = wallet.transactions.all()

    context = {
        "wallet": wallet,
        "group_count": group_count,
        'bankinfo':bankinfo,
        'transactions':transactions
    }
    return render(request,'group/dashboard.html',context)