from profiles.models import Profile

import pytest


@pytest.mark.django_db
def test_profile_model_is_created(create_empty_profile):
    """
    Test if the Profile model is being successfully created
    """
    assert len(Profile.objects.all()) == 1
