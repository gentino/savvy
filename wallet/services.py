# wallet/services.py

from django.db import transaction
from .models import WalletTransaction
from deposits.models import Deposit
from withdrawals.models import Withdrawal
from notifications.models import Notification
from wallet.models import Wallet
from decimal import Decimal


def approve_deposit(deposit):

    with transaction.atomic():

        # Prevent approving the same deposit twice
        if deposit.status != Deposit.PENDING:
            return False, "This deposit has already been processed."

        # Get the user's wallet
        wallet = deposit.user.wallet

        # Record balance before
        balance_before = wallet.balance

        # Credit wallet
        wallet.balance += deposit.amount
        wallet.total_deposited += deposit.amount

        # Record balance after
        balance_after = wallet.balance

        wallet.save(
            update_fields=[
                "balance",
                "total_deposited",
                "updated_at",
            ]
        )

        # Create wallet transaction
        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=WalletTransaction.DEPOSIT,
            amount=deposit.amount,
            balance_before=balance_before,
            balance_after=balance_after,
            status=WalletTransaction.SUCCESSFUL,
            description=f"Deposit {deposit.transaction_reference} approved",
            gateway_reference=deposit.transaction_reference,
        )

        # Mark deposit successful
        deposit.status = Deposit.SUCCESSFUL
        deposit.save(update_fields=["status", "updated_at"])
        
        Notification.objects.create(
        user=deposit.user,
        type=Notification.DEPOSIT_APPROVED,
        amount=deposit.amount
)

    return True, "Deposit approved successfully."

def reject_deposit(deposit):
    
    with transaction.atomic():

        if deposit.status != Deposit.PENDING:
            return False, "This deposit has already been processed."

        deposit.status = Deposit.FAILED
        deposit.save(update_fields=["status", "updated_at"])
        
        Notification.objects.create(
        user=deposit.user,
        type=Notification.DEPOSIT_REJECTED,
        amount=deposit.amount)

    return True, "Deposit rejected successfully."



def approve_withdrawal(withdrawal):

    with transaction.atomic():

        # Prevent processing twice
        if withdrawal.status != Withdrawal.PENDING:
            return False, "This withdrawal has already been processed."

        # Get user's wallet
        wallet = withdrawal.user.wallet

        # Make sure the wallet has enough money
        if wallet.balance < withdrawal.amount:
            return False, "Insufficient wallet balance."

        # Balance before withdrawal
        balance_before = wallet.balance

        # Deduct from wallet
        wallet.balance -= withdrawal.amount
        wallet.total_withdrawn += withdrawal.amount

        # Balance after withdrawal
        balance_after = wallet.balance

        wallet.save(
            update_fields=[
                "balance",
                "total_withdrawn",
                "updated_at",
            ]
        )

        # Record wallet transaction
        WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=WalletTransaction.WITHDRAWAL,
            amount=withdrawal.amount,
            balance_before=balance_before,
            balance_after=balance_after,
            status=WalletTransaction.SUCCESSFUL,
            description="Withdrawal approved",
        )

        # Mark withdrawal successful
        withdrawal.status = Withdrawal.SUCCESSFUL
        withdrawal.save(update_fields=["status", "updated_at"])
        # Notify user
        Notification.objects.create(
            user=withdrawal.user,
            type=Notification.WITHDRAWAL_APPROVED,
            amount=withdrawal.amount)

    return True, "Withdrawal approved successfully."


def reject_withdrawal(withdrawal):
    
    with transaction.atomic():

        if withdrawal.status != Withdrawal.PENDING:
            return False, "This withdrawal has already been processed."

        withdrawal.status = Withdrawal.FAILED

        withdrawal.save(
            update_fields=["status","updated_at",])
        
        Notification.objects.create(
        user=withdrawal.user,
        type=Notification.WITHDRAWAL_REJECTED,
        amount=withdrawal.amount)

    return True, "Withdrawal rejected successfully."



PLATFORM_FEE_PERCENT = Decimal("2.00")


def group_payout(savings):

    group = savings.group
    member = savings.user

    # Current savings cycle
    total_fund = savings.balance

    if total_fund <= Decimal("0.00"):
        return False, "No funds available for payout."

    # -----------------------------------------
    # SAVVY PLATFORM FEE
    # -----------------------------------------

    platform_fee = (
        total_fund
        * PLATFORM_FEE_PERCENT
        / Decimal("100")
    )

    # Amount remaining after Savvy's 2%
    available_fund = total_fund - platform_fee

    # -----------------------------------------
    # GROUP CREATOR COMMISSION
    # -----------------------------------------

    commission = (
        available_fund
        * group.group_commission
        / Decimal("100")
    )

    # -----------------------------------------
    # MEMBER PAYOUT
    # -----------------------------------------

    member_payout = available_fund - commission

    with transaction.atomic():

        # Lock wallets so two payout processes
        # cannot modify them at the same time.
        member_wallet = Wallet.objects.select_for_update().get(
            user=member
        )

        creator_wallet = Wallet.objects.select_for_update().get(
            user=group.creator
        )

    
        # MEMBER WALLET

        member_before = member_wallet.balance
        member_wallet.balance += member_payout
        member_wallet.save(
            update_fields=[
                "balance",
                "updated_at"
            ]
        )

        WalletTransaction.objects.create(
            wallet=member_wallet,
            transaction_type=WalletTransaction.ADJUSTMENT,
            amount=member_payout,
            balance_before=member_before,
            balance_after=member_wallet.balance,
            status=WalletTransaction.SUCCESSFUL,
            description=f"Group payout - {group.name}"
        )

        
        # CREATOR WALLET

        creator_before = creator_wallet.balance

        creator_wallet.balance += commission

        creator_wallet.save(
            update_fields=[
                "balance",
                "updated_at"
            ]
        )

        WalletTransaction.objects.create(
            wallet=creator_wallet,
            transaction_type=WalletTransaction.ADJUSTMENT,
            amount=commission,
            balance_before=creator_before,
            balance_after=creator_wallet.balance,
            status=WalletTransaction.SUCCESSFUL,
            description=f"Group commission - {group.name}"
        )

           # COMPLETE CURRENT SAVINGS CYCLE
    

        savings.balance = Decimal("0.00")

        savings.total_withdrawn += member_payout

        savings.save(
            update_fields=[
                "balance",
                "total_withdrawn",
                "updated_at"
            ]
        )

    return True, member_payout