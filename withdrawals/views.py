from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from .forms import BankForm, WithdrawalForm
from .models import BankInfo
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from wallet.models import Wallet, WalletTransaction
from django.db import transaction
from .models import Withdrawal
# Create your views here.

@login_required
def withdrawals(request):

    bankinfo = get_object_or_404(
        BankInfo,
        user=request.user
    )

    if request.method == "POST":

        form = WithdrawalForm(request.POST)

        if form.is_valid():

            withdrawal_request = form.save(commit=False)

            withdrawal_request.user = request.user
            withdrawal_request.status = withdrawal_request.PENDING

            withdrawal_request.save()

            # Create notification
            Notification.objects.create(
                user=request.user,
                type="withdrawal"
            )

            messages.success(
                request,
                "Withdrawal successfully submitted and is awaiting approval."
            )

            return redirect("wallet")

    else:
        form = WithdrawalForm()

    context = {
        "bankinfo": bankinfo,
        "form": form,
    }

    return render(
        request,
        "group/withdraw.html",
        context
    )

@login_required
def confirm(request, id):

    withdrawal = get_object_or_404(
        Withdrawal,
        id=id
    )

    if request.method == "POST":

        with transaction.atomic():

            # Prevent approving the same withdrawal twice
            if withdrawal.status != Withdrawal.Status.PENDING:
                messages.error(
                    request,
                    "This withdrawal has already been processed."
                )
                return redirect("withdrawal_notification")

            wallet = Wallet.objects.select_for_update().get(
                user=withdrawal.user
            )

            # Make sure the user has enough money
            if wallet.balance < withdrawal.amount:
                messages.error(
                    request,
                    "Insufficient wallet balance."
                )
                return redirect("withdrawal_notification")

            # Deduct money from personal wallet
            wallet.balance -= withdrawal.amount
            wallet.save(update_fields=["balance"])

            # Create wallet transaction
            WalletTransaction.objects.create(
                wallet=wallet,
                amount=withdrawal.amount,
                transaction_type=WalletTransaction.WITHDRAWAL,
                status=WalletTransaction.COMPLETED,
                description="Withdrawal approved"
            )

            # Approve withdrawal
            withdrawal.status = Withdrawal.Status.APPROVED
            withdrawal.save(
                update_fields=["status", "updated_at"]
            )

            # Notify user
            Notification.objects.create(
                user=withdrawal.user,
                type=Notification.WITHDRAWAL_APPROVED
            )

        messages.success(
            request,
            "Withdrawal approved and wallet transaction completed."
        )

        return redirect("withdrawal_notification")

    return redirect("withdrawal_notification")

@login_required
def reject(request, id):

    withdrawal = get_object_or_404(
        Withdrawal,
        id=id
    )

    if request.method == "POST":

        with transaction.atomic():

            if withdrawal.status != Withdrawal.Status.PENDING:
                messages.error(
                    request,
                    "This withdrawal has already been processed."
                )
                return redirect("withdrawal_notification")

            withdrawal.status = Withdrawal.Status.REJECTED

            withdrawal.save(
                update_fields=["status", "updated_at"]
            )

            Notification.objects.create(
                user=withdrawal.user,
                type=Notification.WITHDRAWAL_REJECTED
            )

        messages.success(
            request,
            "Withdrawal rejected successfully."
        )

        return redirect("withdrawal_notification")

    return redirect("withdrawal_notification")

def add_bank(request):
    
    if request.method=='POST':
        form=BankForm(request.POST)
        if form.is_valid():
            bank_details = form.save(commit=False)
            bank_details.user = request.user
            bank_details.save()
            messages.success(request,'Details added successfull')
            return redirect('wallet')
    else:
        form=BankForm()
    return render(request,'group/withdrawal_details.html',{'form':form})


def edit_bank(request):
    bankinfo=get_object_or_404(BankInfo,user=request.user)
    
    if request.method=='POST':
        form=BankForm(request.POST,instance=bankinfo)
        if form.is_valid():
            bank_details = form.save(commit=False)
            bank_details.user = request.user
            bank_details.save()
            messages.success(request,'Details added successfull')
            return redirect('wallet')
    else:
        form=BankForm(instance=bankinfo)
    return render(request,'group/withdrawal_details.html',{'form':form})
