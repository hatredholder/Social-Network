from .models import Profile, Relationship


def get_request_user_profile(request_user):
    user = Profile.objects.get(user=request_user)
    return user

def get_profile_by_pk(request):
    pk = request.POST.get('profile_pk')
    profile = Profile.objects.get(pk=pk)
    return profile

def get_received_invites(profile):
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    return results

def get_sent_invites(profile):
    qs = Relationship.objects.invitations_sent(profile)
    results = list(map(lambda x: x.receiver, qs))
    return results

def follow_unfollow(my_profile, profile):
    if profile.user in my_profile.following.all():
        my_profile.following.remove(profile.user)
    else:
        my_profile.following.add(profile.user)