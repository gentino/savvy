from django.shortcuts import render, redirect, get_object_or_404,get_list_or_404
from .models import Group,GroupMember,GroupInviteLink,JoinRequest
from django.contrib import messages
from .forms import GroupForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from decimal import Decimal
from django.db import transaction
from wallet.models import GroupSavings
from django.db.models import Sum, Q, Case, When, Value, BooleanField,Count,F,Value,ExpressionWrapper,IntegerField
from wallet.models import Wallet, WalletTransaction
from django.http import Http404
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def groups(request):
    # groups = Group.objects.filter(creator=request.user)
    groups = Group.objects.filter(Q(creator=request.user) | Q(group_members__user=request.user,
        group_members__status=GroupMember.ACTIVE)).distinct().annotate(
        is_creator=Case(
        When(creator=request.user, then=Value(True)),
        default=Value(False),
        output_field=BooleanField()),
        
        # Active members, excluding creator
        active_member_count=Count(
        "group_members",
        filter=Q(
            group_members__role=GroupMember.MEMBER,
            group_members__status=GroupMember.ACTIVE)),
        remaining_slots=ExpressionWrapper(
        F("max_members") - F("active_member_count"),
        output_field=IntegerField())
        
        )
    context = {
         'groups':groups
    }
    return render(request, "group/groups.html",context)

def create(request):
    if request.method == "POST":
        form=GroupForm(request.POST,request.FILES)
        if form.is_valid():
            group= form.save(commit=False)
            group.creator=request.user
            group.is_active= True
            group.save()
            
            GroupMember.objects.create(
            group=group,
            user=request.user,
            role=GroupMember.CREATOR,
            status=GroupMember.ACTIVE,
        )
            messages.success(request,"Group successfully created!!!")
            return redirect('groups')
    else:
        form=GroupForm()

    context={
        'form':form
    }
    return render(request, "group/create_group.html",context)


def group_details(request, id):
    group = get_object_or_404(Group,id=id)
    
    if (group.creator != request.user and not GroupMember.objects.filter(group=group,user=request.user,status=GroupMember.ACTIVE).exists()):
        raise Http404
    is_creator = group.creator == request.user
    invite_link, created = GroupInviteLink.objects.get_or_create(group=group)
    invite_url = request.build_absolute_uri(
        reverse("group_invite", kwargs={ "token": invite_link.token})
    )
    # member = group.members.filter(is_active=True,role='member').count()
    member = group.group_members.filter(status=GroupMember.ACTIVE,role=GroupMember.MEMBER).count()
    savings = GroupSavings.objects.filter(group=group,user=request.user).first()
        
    match group.contribution_frequency:
        case "daily":
            frequency_days = 1

        case "weekly":
            frequency_days = 7

        case "monthly":
            frequency_days = 30

        case _:
            frequency_days = 0
    
    if group.creator == request.user:
        target=group.contribution_amount * (Decimal(group.duration)/frequency_days) * member
        total_saved = GroupSavings.objects.filter(group=group).aggregate(
        total=Sum("total_contributed"))["total"] or 0
    else:
        target=group.contribution_amount * (Decimal(group.duration)/frequency_days) 
        total_saved = savings.total_contributed if savings else 0
    
    

    if target > 0:
        progress = (total_saved / target) * Decimal("100")
    else:
        progress = Decimal("0")

    # Don't allow the chart to go above 100%
    progress = min(progress, Decimal("100"))
    savings = GroupSavings.objects.filter(
    group=group,
    user=request.user
).first()

    can_contribute = True
    next_contribution=None

    if savings and savings.last_contributed_at:

        now = timezone.now()

        if group.contribution_frequency == Group.DAILY:
            next_contribution = (
                savings.last_contributed_at + timedelta(days=1)
            )

        elif group.contribution_frequency == Group.WEEKLY:
            next_contribution = (
                savings.last_contributed_at + timedelta(weeks=1)
            )

        elif group.contribution_frequency == Group.MONTHLY:
            next_contribution = (
                savings.last_contributed_at + relativedelta(months=1)
            )

        else:
            next_contribution = now

        if now < next_contribution:
            can_contribute = False
    context = {
        'group':group,
        "invite_link": invite_link,
        "invite_url": invite_url,
        'target':target,
        'total_saved':total_saved,
        'progress':progress,
        'is_creator':is_creator,
        'member_count':member,
        'can_contribute':can_contribute,
        'next_contribution':next_contribution
    }
    return render(request, "group/group.html",context)

def delete(request,id):
    group =get_object_or_404(Group,id=id)
    group.delete()
    messages.success(request,'Group deleted successfully')
    return redirect('groups')


def edit_group(request,id):
    pass

@login_required
def group_invite(request,token):
    invite_link = get_object_or_404(GroupInviteLink.objects.select_related("group"),token=token)
    group = invite_link.group

    # Check whether the invite link is still valid
    if not invite_link.is_valid():
        return render(request,"groups/group/manage/invite_expired.html",{"group": group})

    # Prevent inactive groups from accepting requests
    if not group.is_active:
        return render(request,"groups/group/manage/invite_expired.html",{"group": group,})
    
    
    yearly_contribution=group.contribution_amount * group.duration
    context ={
              "group": group,
              "invite_link": invite_link,
              'yearly_contribution':yearly_contribution
              }
   

    return render(request,"group/manage/group_invite.html",context)




@login_required
def join_group(request, token):

    if request.method != "POST":
        return redirect("group_invite", token=token)

    # Get invite link
    invite_link = get_object_or_404(GroupInviteLink.objects.select_related("group"),token=token)
    group = invite_link.group
    
    # Check invite link
    if not invite_link.is_valid():
        messages.error(request,"This invitation link is no longer valid.")
        return redirect("group_invite",token=token)

    # Check group
  
    if not group.is_active:
        messages.error(request,"This group is no longer active.")
        return redirect("group_invite",token=token)


    # Creator cannot join their own group
   

    if group.creator == request.user:
        messages.info(request,"You are already the creator of this group.")
        return redirect("group_invite",token=token)

    # Check existing membership

    existing_member = GroupMember.objects.filter(group=group,user=request.user,status=GroupMember.ACTIVE).first()
    if existing_member:
        if existing_member.status == GroupMember.ACTIVE:
            messages.info(request,"You are already a member of this group.")

        elif existing_member.status == GroupMember.REMOVED:
            messages.error(request,"You have been removed from this group.")
        elif existing_member.status == GroupMember.LEFT:
            messages.info(request,"You previously left this group.")
        return redirect("group_invite",token=token)

    # Check group capacity
    active_members = GroupMember.objects.filter(
        group=group,
        status=GroupMember.ACTIVE
    ).count()

    if active_members >= group.max_members:
        messages.error(request,"This group has reached its maximum number of members.")
        return redirect("group_invite",token=token)

    # Check existing pending request
    existing_request = JoinRequest.objects.filter(group=group,user=request.user,status=JoinRequest.PENDING).first()

    if existing_request:
        messages.info(request,"You have already requested to join this group.")
        return redirect("group_invite",token=token)
    
    # Get optional message
    message =f'{request.user.last_name} {request.user.first_name}  sent you a request to join the group you manage' 

    # Create join request
    JoinRequest.objects.create(
        group=group,
        user=request.user,
        invite_link=invite_link,
        message=message,
        status=JoinRequest.PENDING
    )
    messages.success(request,"Your request to join has been sent.")
    return redirect("group_invite",token=token)


def group_invites(request,id):
    invites = JoinRequest.objects.filter(group=id)
    pending=invites.filter(status=JoinRequest.PENDING).count()
    rejected=invites.filter(status=JoinRequest.REJECTED).count()
    approved=invites.filter(status=JoinRequest.APPROVED).count()
    group=Group.objects.get(id=id)
    
    context ={
        'invites':invites,
        'pending':pending,
        'rejected':rejected,
        'approved':approved,
        'group': group
    }
    return render(request,'group/manage/invites.html',context)


def group_members(request,id):
    group=get_object_or_404(Group,id=id)
    # members=group.members.filter(role='member')
    members = GroupMember.objects.filter(group=group,role='member',status=GroupMember.ACTIVE).select_related('user')
    context = {
        'group':group,
        'members':members
    }
    return render(request,'group/manage/members.html',context)






@login_required
def approve_join_request(request, id):

    if request.method != "POST":
        return redirect("invites", id=id)

    join_request = get_object_or_404(
        JoinRequest.objects.select_related("group","user"),id=id)
    group = join_request.group

    # Only the group creator can approve requests
    if group.creator != request.user:
        messages.error(request,"You do not have permission to approve this request.")
        return redirect("invites",id=group.id)

    # Request must still be pending
    if join_request.status != JoinRequest.PENDING:

        messages.warning(request,"This join request has already been processed.")
        return redirect("invites",id=group.id)

    # Check group capacity
    active_members = GroupMember.objects.filter(group=group,status=GroupMember.ACTIVE).count()
    if active_members >= group.max_members:
        messages.error(request,"This group has reached its maximum number of members.")
        return redirect("invites",id=group.id)
    
    with transaction.atomic():
        # Create membership
        membership, created = GroupMember.objects.get_or_create(
        group=group,
        user=join_request.user,
        defaults={
            "role": GroupMember.MEMBER,
            "status": GroupMember.ACTIVE,
        })

        if not created:
            membership.status = GroupMember.ACTIVE
            membership.role = GroupMember.MEMBER
            membership.left_at = None

            membership.save(
                update_fields=[
                    "status",
                    "role",
                    "left_at"
                ]
            )
        
        


        join_request.delete()

    messages.success(request,f"{join_request.user.get_full_name()} has been added to the group.")
    return redirect("invites",id=group.id)


@login_required
def reject_join_request(request, id):

    if request.method != "POST":
        return redirect("invites", id=id)
    join_request = get_object_or_404(JoinRequest.objects.select_related("group","user"),id=id)
    group = join_request.group
    
    # Only the creator can reject requests
    if group.creator != request.user:
        messages.error(request,"You do not have permission to reject this request.")
        return redirect("invites",id=group.id)

    # Request must still be pending
    if join_request.status != JoinRequest.PENDING:
        messages.warning(request,"This join request has already been processed.")

        return redirect("invites",id=group.id)
    
    # join_request.status = JoinRequest.REJECTED
    # join_request.reviewed_at = timezone.now()

    # join_request.save(update_fields=["status","reviewed_at"])
    
    join_request.delete()
    messages.success(request,f"{join_request.user.get_full_name()} has been declined.")

    return redirect("invites",id=group.id)



@login_required
def leave_group(request, id):
    group = get_object_or_404(Group, id=id)
    membership = get_object_or_404(GroupMember,group=group,user=request.user,role=GroupMember.MEMBER)
    if request.method == "POST":
        membership.status = GroupMember.LEFT
        membership.save(update_fields=["status"])
        messages.success(request,f"You have left {group.name}.")
        return redirect("groups")
    return redirect("group", id=group.id)

@login_required
def remove_member(request, id, user_id):
    group = get_object_or_404(Group, id=id)

    # Only the creator can remove members
    if group.creator != request.user:
        messages.error(request,"Only the group creator can remove members.")
        return redirect("group", id=group.id)
    membership = get_object_or_404(GroupMember,group=group,user_id=user_id,role=GroupMember.MEMBER)
    if request.method == "POST":
        with transaction.atomic():
            # Lock the wallet while performing the refund
            wallet = Wallet.objects.select_for_update().get(user=membership.user)
        
            # Get the member's group savings
            savings = GroupSavings.objects.select_for_update().filter(group=group,user=membership.user).first()
            refund_amount = (savings.balance if savings else Decimal("0.00"))
            
            
            # Return group balance to user's wallet
            if refund_amount > Decimal("0.00"):
                wallet.balance += refund_amount
                wallet.save(update_fields=["balance"])

                # Record the amount withdrawn from group savings
                savings.balance = Decimal("0.00")
                savings.total_withdrawn += refund_amount

                savings.save(
                    update_fields=["balance","total_withdrawn","updated_at",])

                # Record wallet transaction
                WalletTransaction.objects.create(
                    user=membership.user,
                    amount=refund_amount,
                    transaction_type="group_refund",
                    status="completed"
                )

        membership.status = GroupMember.REMOVED
        membership.save(update_fields=["status"])
        messages.success(request,f"{membership.user.username} has been removed from the group.")
    return redirect("group", id=group.id)
