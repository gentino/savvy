from django.urls import path
from .import views


urlpatterns = [
    path('all',views.groups,name="groups"),
    path('create',views.create,name="create_group"),
    path('group/<int:id>',views.group_details,name="group"),
    path('delete/<int:id>',views.delete,name="delete_group"),
    path("invite/<uuid:token>/",views.group_invite,name="group_invite"),
    path("invite/<uuid:token>/join/",views.join_group,name="join_group"),
    path("invites/<int:id>",views.group_invites,name="invites"),
    path('members/<int:id>',views.group_members,name='group_members'),
    path("group/join-request/<int:id>/approve/",views.approve_join_request,name="approve_join_request"),
    path("group/join-request/<int:id>/reject/",views.reject_join_request,name="reject_join_request"),
    path("groups/<int:id>/leave/",views.leave_group,name="leave_group"),
    path("groups/<int:id>/remove-member/<int:user_id>/",views.remove_member,name="remove_member"),
    path("group/<int:id>/settings/",views.group_settings,name="group_settings"),
]
