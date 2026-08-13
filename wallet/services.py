# wallet/services.py

from django.db import transaction
from .models import WalletTransaction
from deposits.models import Deposit
from withdrawals.models import Withdrawal
from notifications.models import Notification


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