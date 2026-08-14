from django.shortcuts import render,redirect , get_object_or_404
from .models import Notification
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from withdrawals.models import Withdrawal


@login_required
def notifications(request):
    nots=Notification.objects.filter(user=request.user)
     # Count unread notifications BEFORE marking them as read

    unread_count = nots.filter(is_read=False).count()
    
    # Evaluate notifications BEFORE updating the database
    all_nots = list(nots)

    # Mark all notifications as read
    nots.filter(is_read=False).update(is_read=True)
    
    context={
        'notifications':all_nots,
        'unread_count': unread_count,
        
    }
    return render(request, "group/notifications.html",context)


@login_required
def delete_notification(request, id):

    if request.method == "POST":

        notification = get_object_or_404(Notification,id=id,user=request.user)
        notification.delete()
        messages.success(request,'Notification was deleted!!!')

    return redirect("notifications")

@login_required
def read(request,id):
    notification=get_object_or_404(Notification,id=id)
    notification.status=True
    context={'notification':notification}
    return render(request, "group/notification/notification.html",context)

@login_required
def delete(request,id):
    notification=get_object_or_404(Notification,id=id)
    notification.delete()
    messages.success(request,'Notification Deleted')
    return redirect('notifications')

