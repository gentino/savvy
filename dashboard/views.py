from django.shortcuts import render,get_object_or_404
from groups.models import Group
from withdrawals.models import BankInfo
from notifications.models import Notification


# Create your views here.
def dashboard(request):
    bankinfo=BankInfo.objects.filter(user=request.user).first()
    wallet = request.user.wallet
    group_count = Group.objects.filter(members=request.user).count()
    transactions = wallet.transactions.all()
    notifications=Notification.objects.filter(user=request.user)
    # Count unread notifications BEFORE marking them as read
    unread_count = notifications.filter(is_read=False).count()

    context = {
        "wallet": wallet,
        "group_count": group_count,
        'bankinfo':bankinfo,
        'transactions':transactions,
        'unread_count':unread_count
    }
    return render(request,'group/dashboard.html',context)