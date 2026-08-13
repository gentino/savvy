from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from notifications.models import Notification
from .forms import DepositForm


@login_required
def deposit(request):

    if request.method == "POST":

        form = DepositForm(request.POST)

        if form.is_valid():

            # Create the deposit
            deposit = form.save(commit=False)

            # Attach deposit to logged-in user
            deposit.user = request.user

            # Deposit remains pending until admin approval
            deposit.status = deposit.PENDING

            deposit.save()

            # Create notification
            Notification.objects.create(user=request.user, type=Notification.DEPOSIT)

            messages.success(
                request,
                "Your deposit request has been submitted successfully "
                "and is awaiting approval.",
            )

            return redirect("wallet")

    else:
        form = DepositForm()

    return render(request, "group/deposit.html", {"form": form})


@login_required
def deposits(request):

    notifications = Notification.objects.filter(
        user=request.user, type=Notification.DEPOSIT
    )

    return render(
        request, "group/notifcations/deposit.html", {"notifications": notifications}
    )


# Create your views here.
