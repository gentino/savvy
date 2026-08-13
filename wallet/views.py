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

# Create your views here.

def wallet(request):
    
    wallet = request.user.wallet
    bankinfo=BankInfo.objects.filter(user=request.user).first()
    transactions = wallet.transactions.all()
    context = {
        'bankinfo':bankinfo,
        "wallet": wallet,
        'transactions':transactions
        
    }
    return render(request,'group/wallet.html',context)



@login_required
def save(request, id):

    group = get_object_or_404(
        Group,
        id=id,
        is_active=True
    )

    # Get the user's personal wallet
    wallet = get_object_or_404(
        Wallet,
        user=request.user
    )

    # Get or create the user's savings for this group
    savings, created = GroupSavings.objects.get_or_create(
        group=group,
        user=request.user
    )

    # The contribution amount comes directly from the group
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


    # MAKE SURE AMOUNT IS VALID
    if amount <= Decimal("0.00"):
        messages.error(
            request,
            "This group has an invalid contribution amount."
        )
        return redirect("group", id=group.id)

    # Check wallet balance
    if wallet.balance < amount:
        messages.error(
            request,
            f"Insufficient wallet balance. "
            f"You need ₦{amount:,.2f} to make this contribution."
        )
        return redirect("group", id=group.id)

    with transaction.atomic():

        now = timezone.now()

        # Deduct from personal wallet
        wallet.balance -= amount
        wallet.save(update_fields=["balance"])

        # Add to group savings
        savings.balance += amount
        savings.total_contributed += amount

        # IMPORTANT: record this contribution time
        savings.last_contributed_at = now

        savings.save()

        # Record wallet transaction
        balance_before = wallet.balance

        # Deduct from wallet
        wallet.balance -= amount

        balance_after = wallet.balance

        wallet.save(update_fields=["balance"])

        WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type="contribution",
            status="completed",
            balance_before=balance_before,
            balance_after=balance_after,
            description=f"Contribution to {group.name}"
        )

    messages.success(request,f"Your contribution of ₦{amount:,.2f} was successful.")
    return redirect("group", id=group.id)

@login_required
def transactions(request):
    wallet = get_object_or_404(Wallet,user=request.user)
    transactions = wallet.transactions.all()
    return render(request,"wallet/transactions.html",{"transactions": transactions})