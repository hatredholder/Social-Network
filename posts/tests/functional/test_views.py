from django.contrib.auth.models import User

from profiles.models import Profile

import pytest

from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_post_comment_create_and_list_view_template_used(create_test_user, client):
    client.force_login(user=create_test_user)

    response = client.get('/posts/')

    assert response.status_code == 200
    assertTemplateUsed(response, "posts/main.html")


@pytest.mark.django_db
def test_post_comment_create_and_list_view_related_post(client, create_test_post, create_test_user):
    
    # Add testuser to user friend list
    Profile.objects.get(user=create_test_user).friends.add(User.objects.get(username="user"))

    client.force_login(user=create_test_user)

    response = client.get('/posts/')

    assert b"test post content" in response.content
