from django.contrib.auth.models import User

from posts.models import Post

from profiles.models import Profile

import pytest


@pytest.fixture
def create_empty_profile():
    """
    Create an empty profile
    """
    user = User.objects.create(username="testuser")

    # Profile gets created automatically by a signal
    profile = Profile.objects.get(user=user)

    return profile


@pytest.fixture
def create_test_post(create_empty_profile):
    """
    Create a post
    """
    post = Post.objects.create(
        content="test content",
        author=create_empty_profile,
    )
    return post


@pytest.fixture
def create_profile_with_friends_followings(create_empty_profile):
    """
    Creates a profile with a friend in their friendlist
    and with a following
    """
    user = User.objects.create(username="followinguser")
    friend = User.objects.create(username="frienduser")

    profile = Profile.objects.get(user=user)
    profile.following.add(create_empty_profile.user)
    profile.friends.add(friend)

    return profile
