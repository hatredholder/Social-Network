from posts.models import Like
from profiles.models import Profile

import pytest


# Profile model tests


@pytest.mark.django_db
def test_profile_model_is_created(create_empty_profile):
    """
    Test if the Profile model is being successfully created
    """
    assert len(Profile.objects.all()) == 1


@pytest.mark.django_db
def test_profile_model_str_method(create_empty_profile):
    """
    Test if the Profile model str method is working as intended
    """
    assert str(Profile.objects.all().first()) == "user"


@pytest.mark.django_db
def test_profile_model_get_absolute_url_method(create_empty_profile):
    """
    Test if the Profile model get_absolute_url method is working as intended
    """
    assert str(Profile.objects.all().first().get_absolute_url()) == "/profiles/users/user/"


@pytest.mark.django_db
def test_profile_model_get_likes_given_count_method(create_empty_profile, create_test_like):
    """
    Test if the Profile model get_likes_given_count method is working as intended
    """
    assert Profile.objects.all().first().get_likes_given_count() == 1


@pytest.mark.django_db
def test_profile_model_get_likes_received_count_method(create_empty_profile, create_test_post):
    """
    Test if the Profile model get_likes_given_count method is working as intended
    """
    create_test_post.liked.add(create_empty_profile)
    assert Profile.objects.all().first().get_likes_received_count() == 1
