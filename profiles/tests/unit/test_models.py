from django.contrib.auth.models import User

from profiles.models import Message, Profile, Relationship

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
    assert (
        str(Profile.objects.all().first().get_absolute_url()) == "/profiles/users/user/"
    )


@pytest.mark.django_db
def test_profile_model_get_likes_given_count_method(
    create_empty_profile, create_test_like
):
    """
    Test if the Profile model get_likes_given_count method is working as intended
    """
    assert Profile.objects.all().first().get_likes_given_count() == 1


@pytest.mark.django_db
def test_profile_model_get_likes_received_count_method(
    create_empty_profile, create_test_post
):
    """
    Test if the Profile model get_likes_given_count method is working as intended
    """
    create_test_post.liked.add(create_empty_profile)
    assert Profile.objects.all().first().get_likes_received_count() == 1


@pytest.mark.django_db
def test_profile_manager_get_my_friends_profiles_method(create_test_user):
    """
    Test if the Profile model get_likes_given_count method is working as intended
    """
    Profile.objects.get(user=create_test_user).friends.add(
        User.objects.create(username="frienduser"),
    )
    assert len(Profile.objects.get_my_friends_profiles(create_test_user)) == 1


# Relationship model tests


@pytest.mark.django_db
def test_relationship_model_is_created(create_test_relationship):
    """
    Test if the Relationship model is being successfully created
    """
    assert len(Relationship.objects.all()) == 1


@pytest.mark.django_db
def test_relationship_model_str_method(create_test_relationship):
    """
    Test if the Relationship model str method is working as intended
    """
    assert str(Relationship.objects.all().first()) == "user - followinguser - sent"


@pytest.mark.django_db
def test_relationship_manager_invitations_received_method(
    create_test_relationship,
    create_empty_profile,
    create_profile_friends_followings,
):
    """
    Test if the Relationship model invitations_received method is working as intended
    """
    assert len(Relationship.objects.invitations_received(create_empty_profile)) == 0
    assert (
        len(
            Relationship.objects.invitations_received(create_profile_friends_followings)
        )
        == 1
    )


@pytest.mark.django_db
def test_relationship_manager_invitations_sent_method(
    create_test_relationship,
    create_empty_profile,
    create_profile_friends_followings,
):
    """
    Test if the Relationship model invitations_sent method is working as intended
    """
    assert len(Relationship.objects.invitations_sent(create_empty_profile)) == 1
    assert (
        len(Relationship.objects.invitations_sent(create_profile_friends_followings))
        == 0
    )


# Message model tests


@pytest.mark.django_db
def test_message_model_is_created(create_test_message):
    """
    Test if the Message model is being successfully created
    """
    assert len(Message.objects.all()) == 1


@pytest.mark.django_db
def test_message_model_str_method(
    create_empty_profile, create_profile_friends_followings
):
    """
    Test if the Message model str method is working as intended
    """
    short_message = Message.objects.create(
        sender=create_empty_profile,
        receiver=create_profile_friends_followings,
        content="short content",
    )
    long_message = Message.objects.create(
        sender=create_empty_profile,
        receiver=create_profile_friends_followings,
        content="long content long content long content long content long content long content",
    )

    assert str(short_message) == "user - short content"
    assert (
        str(long_message)
        == "user - long content long content long content long conten.."
    )
