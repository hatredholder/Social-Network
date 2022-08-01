from .models import Profile


def get_request_user_profile(request_user):
    """
    Gets Profile model with request.user
    """
    user = Profile.objects.get(user=request_user)
    return user