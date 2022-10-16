from django.contrib.auth.models import User

from posts.models import Comment, Like, Post

from profiles.models import Profile

import pytest


@pytest.fixture
def create_empty_profile():
    """
    Create and return an empty profile
    """
    user = User.objects.create(username="user")

    # Profile gets created automatically by a signal
    profile = Profile.objects.get(user=user)

    return profile


@pytest.fixture
def create_test_user():
    """
    Create and return a User object
    """
    user = User.objects.create(
        username="testuser",
        password="testpass",
        email="testuser@gmail.com",
    )
    return user


@pytest.fixture
def create_test_post(create_empty_profile):
    """
    Create and return a Post object
    """
    post = Post.objects.create(
        content="test post content",
        author=create_empty_profile,
    )
    return post


@pytest.fixture
def create_profile_friends_followings(create_empty_profile):
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


@pytest.fixture
def create_test_comment(create_empty_profile, create_test_post):
    """
    Create and return Comment object
    """
    comment = Comment.objects.create(
        profile=create_empty_profile,
        post=create_test_post,
        content="comment content",
    )
    return comment


@pytest.fixture
def create_test_like(create_empty_profile, create_test_post):
    """
    Create and return Like object
    """
    like = Like.objects.create(
        profile=create_empty_profile,
        post=create_test_post,
    )
    return like
