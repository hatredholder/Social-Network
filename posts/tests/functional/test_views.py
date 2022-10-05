from django.contrib.auth.models import User

from posts.models import Post

from profiles.models import Profile

import pytest

from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_post_comment_create_and_list_view_template_used(create_test_user, client):
    """
    Test if appopriate template is used in view
    """
    client.force_login(user=create_test_user)

    response = client.get('/posts/')

    assert response.status_code == 200
    assertTemplateUsed(response, "posts/main.html")


@pytest.mark.django_db
def test_post_comment_create_and_list_view_related_post(client, create_test_post, create_test_user):
    """
    Test if created related post appears on testuser's posts page
    """
    
    # Add testuser to user friend list
    Profile.objects.get(user=create_test_user).friends.add(User.objects.get(username="user"))

    client.force_login(user=create_test_user)

    response = client.get('/posts/')

    assert b"test post content" in response.content


@pytest.mark.django_db
def test_post_comment_create_and_list_view_post_create(create_test_user, client):
    """
    Test if appopriate template is used in view
    """
    client.force_login(user=create_test_user)

    data = {
        "content": "post content",
        "submit_p_form": "",
    }

    response = client.post('/posts/', data=data)

    assert response.status_code == 302
    assert len(Post.objects.all()) == 1
