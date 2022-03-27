from django.urls import path
from .views import (invites_received_view, 
                    my_profile_view,  
                    invite_profile_list_view, 
                    remove_from_friends,
                    send_invitation,
                    accept_invitation,
                    reject_invitation,
                    follow_unfollow_user,
                    search_profiles,
                    ProfileListView,
                    ProfileDetailView)

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all-profiles-view'),
    path('users/<slug>/', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('myprofile/', my_profile_view, name='my-profile-view'),
    path('search/', search_profiles, name='search-profiles-view'),
    path('my_invites/', invites_received_view, name='my-invites-view'),
    path('sent_invites/', invite_profile_list_view, name='sent-invites-view'),
    path('switch_follow/', follow_unfollow_user, name='follow-unfollow-view'),
    path('send-invite/', send_invitation, name='send-invite'),
    path('remove-friend', remove_from_friends, name='remove-friend'),
    path('my_invites/accept', accept_invitation, name='accept-invite'),
    path('my_invites/reject', reject_invitation, name='reject-invite'),
]
