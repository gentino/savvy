from django.shortcuts import render,redirect , get_object_or_404
from .models import Notification
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from withdrawals.models import Withdrawal



def notifications(request):
    notifcations=Notification.objects.filter(user=request.user)
    context={
        'notifications':notifcations
    }
    return render(request, "group/notifications.html",context)


@login_required
def delete_notification(request, id):

    if request.method == "POST":

        notification = get_object_or_404(Notification,id=id,user=request.user)
        notification.delete()
        messages.success(request,'Notification was deleted!!!')

    return redirect("notifications")


def read(request,id):
    notification=get_object_or_404(Notification,id=id)
    notification.status=True
    context={'notification':notification}
    return render(request, "group/notification/notification.html",context)


def delete(request,id):
    notification=get_object_or_404(Notification,id=id)
    notification.delete()
    messages.success(request,'Notification Deleted')
    return redirect('notifications')

