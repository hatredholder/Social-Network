# Add fixtures from other conftest.py
from posts.tests.conftest import (client, create_empty_profile,  # noqa: F401
                                  create_profile_friends_followings,
                                  create_test_like, create_test_post,
                                  create_test_user)

from profiles.models import Relationship

import pytest


@pytest.fixture
def create_test_relationship(
    create_empty_profile, create_profile_friends_followings,  # noqa: F811
):
    relationship = Relationship.objects.create(
        sender=create_empty_profile,
        receiver=create_profile_friends_followings,
        status='sent',
    )
    return relationship
