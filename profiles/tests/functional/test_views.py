import pytest

from pytest_django.asserts import assertTemplateUsed


# my_profile_view


@pytest.mark.django_db
def test_my_profile_view_template_used(create_test_user, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    response = client.get('/profiles/myprofile/')

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/my_profile.html")


@pytest.mark.django_db
def test_my_profile_view_update(create_test_user, client):
    """
    Test if Profile object gets updated successfully through a POST request
    """
    client.force_login(user=create_test_user)

    data = {
        "bio": "new bio",
    }

    response = client.post('/profiles/myprofile/', data=data)

    assert response.status_code == 302


@pytest.mark.django_db
def test_my_profile_view_check_message(create_test_user, client):
    """
    Test if message sent by the view is right
    """
    client.force_login(user=create_test_user)

    data = {
        "bio": "new bio",
    }

    client.post('/profiles/myprofile/', data=data)

    response = client.get('/profiles/myprofile/')

    assert b'Profile updated successfully!' in response.content


# received_invites_view


@pytest.mark.django_db
def test_received_invites_view_template_used(create_test_user, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    response = client.get('/profiles/received_invites/')

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/received_invites.html")


# sent_invites_view


@pytest.mark.django_db
def test_sent_invites_view_template_used(create_test_user, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    response = client.get('/profiles/sent_invites/')

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/sent_invites.html")
