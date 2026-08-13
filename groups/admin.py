from django.contrib import admin
from .models import (
    Group,
    GroupMember,
    GroupInviteLink,
    JoinRequest,
    GroupAnnouncement,
)


# =========================================================
# GROUP ADMIN
# =========================================================

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "creator",
        "contribution_amount",
        "contribution_frequency",
        "duration",
        "max_members",
        "is_active",
        "created_at",
    )

    list_filter = (
        "contribution_frequency",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "creator__email",
        "creator__username",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Group Information",
            {
                "fields": (
                    "name",
                    "description",
                    "group_image",
                    "creator",
                )
            },
        ),

        (
            "Contribution Settings",
            {
                "fields": (
                    "contribution_amount",
                    "contribution_frequency",
                    "duration",
                    "max_members",
                )
            },
        ),

        (
            "Rules & Status",
            {
                "fields": (
                    "penalty_rules",
                    "is_active",
                )
            },
        ),

        (
            "Date Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


# =========================================================
# GROUP MEMBER ADMIN
# =========================================================

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):

    list_display = (
        "group",
        "user",
        "role",
        "status",
        "joined_at",
        "left_at",
    )

    list_filter = (
        "role",
        "status",
        "joined_at",
    )

    search_fields = (
        "group__name",
        "user__email",
        "user__username",
    )

    ordering = ("-joined_at",)

    readonly_fields = (
        "joined_at",
    )

    fieldsets = (
        (
            "Membership Information",
            {
                "fields": (
                    "group",
                    "user",
                    "role",
                    "status",
                )
            },
        ),

        (
            "Membership Dates",
            {
                "fields": (
                    "joined_at",
                    "left_at",
                )
            },
        ),
    )


# =========================================================
# GROUP INVITE LINK ADMIN
# =========================================================

@admin.register(GroupInviteLink)
class GroupInviteLinkAdmin(admin.ModelAdmin):

    list_display = (
        "group",
        "token",
        "is_active",
        "expires_at",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "created_at",
        "expires_at",
    )

    search_fields = (
        "group__name",
        "token",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "token",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Invite Link",
            {
                "fields": (
                    "group",
                    "token",
                    "is_active",
                    "expires_at",
                )
            },
        ),

        (
            "Date Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


# =========================================================
# JOIN REQUEST ADMIN
# =========================================================

@admin.register(JoinRequest)
class JoinRequestAdmin(admin.ModelAdmin):

    list_display = (
        "group",
        "user",
        "invite_link",
        "status",
        "requested_at",
        "reviewed_at",
    )

    list_filter = (
        "status",
        "requested_at",
        "reviewed_at",
    )

    search_fields = (
        "group__name",
        "user__email",
        "user__username",
        "message",
    )

    ordering = ("-requested_at",)

    readonly_fields = (
        "requested_at",
    )

    fieldsets = (
        (
            "Join Request",
            {
                "fields": (
                    "group",
                    "user",
                    "invite_link",
                    "message",
                    "status",
                )
            },
        ),

        (
            "Request Dates",
            {
                "fields": (
                    "requested_at",
                    "reviewed_at",
                )
            },
        ),
    )


# =========================================================
# GROUP ANNOUNCEMENT ADMIN
# =========================================================

@admin.register(GroupAnnouncement)
class GroupAnnouncementAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "group",
        "author",
        "created_at",
    )

    list_filter = (
        "created_at",
        "group",
    )

    search_fields = (
        "title",
        "message",
        "group__name",
        "author__email",
        "author__username",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Announcement",
            {
                "fields": (
                    "group",
                    "author",
                    "title",
                    "message",
                )
            },
        ),

        (
            "Date Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )