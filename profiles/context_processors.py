from .models import Relationship
from .views_utils import get_request_user_profile


def profile_pic(request):
    if request.user.is_authenticated:
        profile = get_request_user_profile(request.user)

        pic = profile.avatar

        return {"profile_pic": pic}
    return {}


def invitations_received_count(request):
    if request.user.is_authenticated:
        profile = get_request_user_profile(request.user)

        result = Relationship.objects.invitations_received(profile).count()

        return {"invitations_received_count": result}
    return {}
