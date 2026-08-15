
from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid


class Group(models.Model):

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    FREQUENCY_CHOICES = (
        (DAILY, "Daily"),
        (WEEKLY, "Weekly"),
        (MONTHLY, "Monthly"),
    )

    PRIVATE = "private"
    PUBLIC = "public"

    VISIBILITY_CHOICES = (
        (PRIVATE, "Private"),
        (PUBLIC, "Public"),
    )
    

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    group_image = models.ImageField(upload_to="group_images/", blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_groups")
    contribution_amount = models.DecimalField(max_digits=12,decimal_places=2)
    contribution_frequency = models.CharField(max_length=20,choices=FREQUENCY_CHOICES)
    # visibility = models.CharField(max_length=20,choices=VISIBILITY_CHOICES,default=PRIVATE)
    duration = models.PositiveIntegerField(default=20)
    max_members = models.PositiveIntegerField(default=20)
    penalty_rules = models.TextField(blank=True)
    group_commission = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    is_active = models.BooleanField(default=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,through="GroupMember",related_name="joined_groups")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class GroupMember(models.Model):

    CREATOR = "creator"
    MEMBER = "member"

    ROLE_CHOICES = (
        (CREATOR, "Creator"),
        (MEMBER, "Member"),
    )

    ACTIVE = "active"
    LEFT = "left"
    REMOVED = "removed"

    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (LEFT, "Left"),
        (REMOVED, "Removed"),
    )

    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name="group_members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="memberships")
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default=MEMBER)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=ACTIVE)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "user"],
                name="unique_group_member"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.group}"


class GroupInviteLink(models.Model):

    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name="invite_link"
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    is_active = models.BooleanField(
        default=True
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def is_expired(self):

        if self.expires_at is None:
            return False

        return timezone.now() > self.expires_at

    def is_valid(self):

        return (
            self.is_active
            and not self.is_expired()
            and self.group.is_active
        )

    def __str__(self):
        return f"Invite Link - {self.group.name}"



class JoinRequest(models.Model):

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="join_requests"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="join_requests"
    )

    invite_link = models.ForeignKey(
        GroupInviteLink,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="join_requests"
    )

    message = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "user"],
                condition=models.Q(status="pending"),
                name="unique_pending_group_join_request"
            )
        ]
        ordering = ["-requested_at"]

    def __str__(self):
        return f"{self.user} -> {self.group}"

class GroupAnnouncement(models.Model):

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="announcements"
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="group_announcements"
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title