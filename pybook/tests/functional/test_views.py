import pytest

from pytest_django.asserts import assertTemplateUsed


# home_view


def test_home_view_template_used(client):
    """
    Test if the right template is used in view
    """
    response = client.get("/")

    assert response.status_code == 200
    assertTemplateUsed(response, "main/home.html")


@pytest.mark.django_db
def test_home_view_check_redirect(client, create_test_user):
    """
    Test if the view redirects
    """
    client.force_login(user=create_test_user)

    response = client.get("/")

    assert response.status_code == 302
