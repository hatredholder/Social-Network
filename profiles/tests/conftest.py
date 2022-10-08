from django.contrib.auth.models import User
from django.test import Client

# Add fixtures from other conftest.py
from posts.tests.conftest import create_test_like, create_test_post  # noqa: F401

from profiles.models import Profile

import pytest


@pytest.fixture
def create_empty_profile():
    """
    Create an empty profile
    """
    user = User.objects.create(username="user")

    # Profile gets created automatically by a signal
    profile = Profile.objects.get(user=user)

    return profile


@pytest.fixture
def client():
    client = Client()
    return client
