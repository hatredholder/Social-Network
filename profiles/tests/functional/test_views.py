from django.contrib.auth.models import User

from posts.models import Comment, Post

from profiles.models import Message, Profile, Relationship


import pytest

from pytest_django.asserts import assertTemplateUsed


# my_profile_view


@pytest.mark.django_db
def test_my_profile_view_template_used(create_test_user, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    response = client.get("/profiles/myprofile/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/my_profile.html")


@pytest.mark.django_db
def test_my_profile_view_comment_create(create_test_post, client):
    """
    Test if comment gets created successfully
    """
    client.force_login(user=User.objects.get(username="user"))

    post_id = Post.objects.first().pk

    data = {
        "post_id": post_id,
        "content": "test comment content",
        "submit_c_form": "",
    }

    response = client.post("/profiles/myprofile/", data=data)

    assert response.status_code == 302
    assert len(Comment.objects.all()) == 1


@pytest.mark.django_db
def test_my_profile_view_update(create_test_user, client):
    """
    Test if Profile object gets updated successfully through a POST request
    """
    client.force_login(user=create_test_user)

    data = {
        "bio": "new bio",
    }

    response = client.post("/profiles/myprofile/", data=data)

    assert response.status_code == 302


@pytest.mark.django_db
def test_my_profile_view_check_message(create_test_user, client):
    """
    Test if message is sent by the view
    """
    client.force_login(user=create_test_user)

    data = {
        "bio": "new bio",
    }

    client.post("/profiles/myprofile/", data=data)

    response = client.get("/profiles/myprofile/")

    assert b"Profile updated successfully!" in response.content


# received_invites_view


@pytest.mark.django_db
def test_received_invites_view_template_used(create_test_user, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    response = client.get("/profiles/received_invites/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/received_invites.html")


# sent_invites_view


@pytest.mark.django_db
def test_sent_invites_view_template_used(create_test_user, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    response = client.get("/profiles/sent_invites/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/sent_invites.html")


# switch_follow


@pytest.mark.django_db
def test_switch_follow_POST(create_empty_profile, create_test_user, client):
    """
    Test if the view is working correctly
    """
    client.force_login(user=create_test_user)

    # Check if user has 0 followers before POST request
    assert len(create_empty_profile.followers.all()) == 0

    profile_id = Profile.objects.all().first().id

    data = {
        "pk": profile_id,
    }

    client.post("/profiles/switch_follow/", data=data)

    # Check if user has 1 follower after POST request
    assert len(create_empty_profile.followers.all()) == 1

    client.post("/profiles/switch_follow/", data=data)

    # Check if user has 0 followers after second POST request
    assert len(create_empty_profile.followers.all()) == 0


# accept_invitation


@pytest.mark.django_db
def test_accept_invitation_no_relationship(create_test_user, client):
    """
    Test if the view is throwing a 404 error when an incorrent pk is sent
    """
    client.force_login(user=create_test_user)

    profile_pk = Profile.objects.get(user=create_test_user).id

    data = {
        "pk": profile_pk,
    }

    response = client.post("/profiles/received_invites/accept/", data=data)

    assert response.status_code == 404


@pytest.mark.django_db
def test_accept_invitation_accept_relationship(create_test_relationship, client):
    """
    Test if the view works correctly when a correct pk is sent
    """
    client.force_login(user=User.objects.get(username="followinguser"))

    profile_pk = Profile.objects.get(user=User.objects.get(username="user")).id

    data = {
        "pk": profile_pk,
    }

    response = client.post("/profiles/received_invites/accept/", data=data)

    assert response.status_code == 302
    assert len(Profile.objects.get(id=profile_pk).friends.all()) == 1


# reject_invitation


@pytest.mark.django_db
def test_reject_invitation_no_relationship(create_test_user, client):
    """
    Test if the view is throwing a 404 error when an incorrent pk is sent
    """
    client.force_login(user=create_test_user)

    profile_pk = Profile.objects.get(user=create_test_user).id

    data = {
        "pk": profile_pk,
    }

    response = client.post("/profiles/received_invites/reject/", data=data)

    assert response.status_code == 404


@pytest.mark.django_db
def test_reject_invitation_accept_relationship(create_test_relationship, client):
    """
    Test if the view works correctly when a correct pk is sent
    """
    client.force_login(user=User.objects.get(username="followinguser"))

    profile_pk = Profile.objects.get(user=User.objects.get(username="user")).id

    data = {
        "pk": profile_pk,
    }

    response = client.post("/profiles/received_invites/reject/", data=data)

    assert response.status_code == 302
    assert len(Profile.objects.get(id=profile_pk).friends.all()) == 0


# my_friends_view


@pytest.mark.django_db
def test_my_friends_view_template_used(create_test_user, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    response = client.get("/profiles/my_friends/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/my_friends.html")


# search_profiles


@pytest.mark.django_db
def test_search_profiles_template_used(create_test_user, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    response = client.get("/profiles/search/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/search_profiles.html")


@pytest.mark.django_db
def test_search_profiles_search_for_testuser(create_test_user, client):
    """
    Test if the search result view returns testuser's profile
    """
    client.force_login(user=create_test_user)

    response = client.get("/profiles/search/?q=testuser")

    assert response.status_code == 200
    assert b"testuser" in response.content
    assert b"No Bio.." in response.content
    assert b"See Profile" in response.content


# send_invitation


@pytest.mark.django_db
def test_send_invitation_send_relationship(
    create_test_user,
    create_empty_profile,
    client,
):
    """
    Test if the view creates a relationship correctly
    """
    client.force_login(user=create_test_user)

    profile_pk = create_empty_profile.id

    data = {
        "pk": profile_pk,
    }

    response = client.post("/profiles/send-invite/", data=data)

    assert response.status_code == 302
    assert len(Relationship.objects.all()) == 1
    assert Relationship.objects.all().first().status == "sent"


# remove_friend


@pytest.mark.django_db
def test_remove_friend_delete_relationship(create_test_relationship, client):
    """
    Test if the view deletes a relationship correctly
    """
    assert len(Relationship.objects.all()) == 1

    client.force_login(user=User.objects.get(username="followinguser"))

    profile_pk = Profile.objects.get(user=User.objects.get(username="user")).id

    data = {
        "pk": profile_pk,
    }

    response = client.post("/profiles/remove-friend/", data=data)

    assert response.status_code == 302
    assert len(Relationship.objects.all()) == 0


# ProfileDetailView


@pytest.mark.django_db
def test_ProfileDetailView_template_used(
    create_test_user,
    create_empty_profile,
    client,
):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    response = client.get("/profiles/users/user/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/profile_detail.html")


@pytest.mark.django_db
def test_ProfileDetailView_redirect_myprofile(create_test_user, client):
    """
    Test if the view redirects when user tries to reach his own profile details
    """
    client.force_login(user=create_test_user)

    response = client.get("/profiles/users/testuser/")

    assert response.status_code == 302


@pytest.mark.django_db
def test_ProfileDetailView_invitation_sent(create_test_relationship, client):
    """
    Test if the view shows "Waiting for approval" when an invitation is sent
    """
    client.force_login(user=User.objects.get(username="user"))

    response = client.get("/profiles/users/followinguser/")

    assert response.status_code == 200
    assert b"Waiting for approval" in response.content


# ProfileListView


@pytest.mark.django_db
def test_ProfileListView_template_used(create_test_user, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    response = client.get("/profiles/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/profile_list.html")


@pytest.mark.django_db
def test_ProfileListView_invitation_sent(create_test_relationship, client):
    """
    Test if the view shows "Waiting for approval" when an invitation is sent
    """
    client.force_login(user=User.objects.get(username="user"))

    response = client.get("/profiles/")

    assert response.status_code == 200
    assert b"Waiting for approval" in response.content


# MessengerListView


@pytest.mark.django_db
def test_MessengerListView_template_used(create_test_user, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    response = client.get("/profiles/messenger/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/messenger.html")


# ChatMessageView


@pytest.mark.django_db
def test_ChatMessageView_template_used(create_profile_friends_followings, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=User.objects.get(username="followinguser"))

    profile_slug = Profile.objects.get(
        user=User.objects.get(username="frienduser"),
    ).slug

    response = client.get(f"/profiles/chat/{profile_slug}/")

    assert response.status_code == 200
    assertTemplateUsed(response, "profiles/chat.html")


@pytest.mark.django_db
def test_ChatMessageView_send_message(create_profile_friends_followings, client):
    """
    Test if the view message sending works correctly
    """
    client.force_login(user=User.objects.get(username="followinguser"))

    profile_slug = Profile.objects.get(
        user=User.objects.get(username="frienduser"),
    ).slug

    data = {
        "content": "test content",
    }

    response = client.post(f"/profiles/chat/{profile_slug}/", data=data)

    assert response.status_code == 302
    assert len(Message.objects.all()) == 1
