from django.shortcuts import render
from withdrawals.models import BankInfo
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from groups.models import Group
from .models import Wallet, WalletTransaction, GroupSavings
from notifications.models import Notification
from wallet.services import group_payout

# Create your views here.
@login_required
def wallet(request):
    
    wallet = request.user.wallet
    bankinfo=BankInfo.objects.filter(user=request.user).first()
    transactions = wallet.transactions.all()
    notifications=Notification.objects.filter(user=request.user)
    # Count unread notifications BEFORE marking them as read
    unread_count = notifications.filter(is_read=False).count()
    context = {
        'bankinfo':bankinfo,
        "wallet": wallet,
        'transactions':transactions,
        'unread_count':unread_count
        
    }
    return render(request,'group/wallet.html',context)



@login_required
def save(request, id):

    group = get_object_or_404(
        Group,
        id=id,
        is_active=True
    )

    # Get user's wallet
    wallet = get_object_or_404(
        Wallet,
        user=request.user
    )

    # Get or create savings
    savings, created = GroupSavings.objects.get_or_create(
        group=group,
        user=request.user
    )

    # Contribution amount
    amount = group.contribution_amount

    # CHECK CONTRIBUTION FREQUENCY

    if savings.last_contributed_at:

        now = timezone.now()

        if group.contribution_frequency == Group.DAILY:

            next_contribution = (
                savings.last_contributed_at
                + timedelta(days=1)
            )

        elif group.contribution_frequency == Group.WEEKLY:

            next_contribution = (
                savings.last_contributed_at
                + timedelta(weeks=1)
            )

        elif group.contribution_frequency == Group.MONTHLY:

            next_contribution = (
                savings.last_contributed_at
                + relativedelta(months=1)
            )

        else:

            messages.error(
                request,
                "Invalid contribution frequency."
            )

            return redirect("group", id=group.id)

        if now < next_contribution:

            messages.warning(
                request,
                "You have already contributed for this period. "
                "Please wait until your next contribution period."
            )

            return redirect("group", id=group.id)

    # VALIDATE CONTRIBUTION AMOUNT
   
    if amount <= Decimal("0.00"):

        messages.error(
            request,
            "This group has an invalid contribution amount."
        )

        return redirect("group", id=group.id)

    
    # CHECK WALLET BALANCE
    if wallet.balance < amount:

        messages.error(
            request,
            f"Insufficient wallet balance. "
            f"You need ₦{amount:,.2f} to make this contribution."
        )

        return redirect("group", id=group.id)

    # MAKE CONTRIBUTION
  
    with transaction.atomic():

        now = timezone.now()

        # Wallet balance BEFORE deduction
        balance_before = wallet.balance

        # Deduct contribution ONCE
        wallet.balance -= amount

        # Wallet balance AFTER deduction
        balance_after = wallet.balance

        wallet.save(
            update_fields=[
                "balance",
                "updated_at"
            ]
        )

        # Add contribution to current savings cycle
        savings.balance += amount

        # Lifetime contribution record
        savings.total_contributed += amount

        # Record contribution time
        savings.last_contributed_at = now

        savings.save()

        # Record wallet transaction
        WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type=WalletTransaction.CONTRIBUTION,
            status=WalletTransaction.SUCCESSFUL,
            balance_before=balance_before,
            balance_after=balance_after,
            description=f"Contribution to {group.name}"
        )

    # CHECK IF TARGET HAS BEEN REACHED

    frequency_days = 0
    if group.contribution_frequency == Group.DAILY:
        frequency_days = 1

    elif group.contribution_frequency == Group.WEEKLY:
        frequency_days = 7

    elif group.contribution_frequency == Group.MONTHLY:
        frequency_days = 30

    if frequency_days > 0:

        target = (
            amount
            * Decimal(group.duration)
            / Decimal(frequency_days)
        )

        if savings.balance >= target:

            success, payout_amount = group_payout(savings)

            if success:
                messages.success(
                    request,
                    f"Congratulations! You reached your savings target. "
                    f"₦{payout_amount:,.2f} has been added to your wallet."
                )

                return redirect(
                    "group",
                    id=group.id
                )

    messages.success(
        request,
        f"Your contribution of ₦{amount:,.2f} was successful."
    )

    return redirect(
        "group",
        id=group.id
    )

@login_required
def transactions(request):
    wallet = get_object_or_404(Wallet,user=request.user)
    transactions = wallet.transactions.all()
    return render(request,"wallet/transactions.html",{"transactions": transactions})