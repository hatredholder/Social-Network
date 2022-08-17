from .models import Profile, Relationship


def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        pic = profile_obj.avatar
        return {'picture':pic}
    return {}

def invitations_received_count(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        qs_count = Relationship.objects.invitations_received(profile_obj).count()
        return {'invitations_received_count':qs_count}
    return {}