from django.contrib.auth.models import User

from posts.models import Comment, Like, Post

from profiles.models import Profile

import pytest

from pytest_django.asserts import assertTemplateUsed


# post_comment_create_and_list_view


@pytest.mark.django_db
def test_post_comment_create_and_list_view_template_used(create_test_user, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    response = client.get("/posts/")

    assert response.status_code == 200
    assertTemplateUsed(response, "posts/main.html")


@pytest.mark.django_db
def test_post_comment_create_and_list_view_related_post(
    client,
    create_test_post,
    create_test_user,
):
    """
    Test if created related post appears on testuser's posts page
    """

    # Add testuser to user friend list
    Profile.objects.get(user=create_test_user).friends.add(
        User.objects.get(username="user"),
    )

    client.force_login(user=create_test_user)

    response = client.get("/posts/")

    assert b"test post content" in response.content


@pytest.mark.django_db
def test_post_comment_create_and_list_view_post_create(create_test_user, client):
    """
    Test if Post object gets created successfully through a POST request
    """
    client.force_login(user=create_test_user)

    data = {
        "content": "post content",
        "submit_p_form": "",
    }

    response = client.post("/posts/", data=data)

    assert response.status_code == 302
    assert len(Post.objects.all()) == 1


@pytest.mark.django_db
def test_post_comment_create_and_list_view_comment_create(
    create_test_user,
    create_test_post,
    client,
):
    """
    Test if Comment object gets created successfully through a POST request
    """
    client.force_login(user=create_test_user)

    post_id = Post.objects.all().first().id

    data = {
        "content": "comment content",
        "post_id": post_id,
        "submit_c_form": "",
    }

    response = client.post("/posts/", data=data)

    assert response.status_code == 302
    assert len(Comment.objects.all()) == 1


# switch_like


@pytest.mark.django_db
def test_switch_like_view_add_like(create_test_user, create_test_post, client):
    """
    Test if Like object gets created successfully through a POST request
    """
    client.force_login(user=create_test_user)

    post_id = Post.objects.all().first().id

    data = {
        "post_id": post_id,
    }

    response = client.post("/posts/like/", data=data)

    assert response.status_code == 200
    assert b'"like_added": true' in response.content
    assert len(Like.objects.all()) == 1


@pytest.mark.django_db
def test_switch_like_view_delete_like(create_test_user, create_test_post, client):
    """
    Test if sending POST request twice deletes the Like object
    """
    client.force_login(user=create_test_user)

    post_id = Post.objects.all().first().id

    data = {
        "post_id": post_id,
    }

    client.post("/posts/like/", data=data)
    assert len(Like.objects.all()) == 1

    client.post("/posts/like/", data=data)
    assert len(Like.objects.all()) == 0


# PostDeleteView


@pytest.mark.django_db
def test_PostDeleteView_template_used(create_test_user, create_test_post, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    post_id = Post.objects.all().first().id

    response = client.get(f"/posts/{post_id}/delete/")

    assert response.status_code == 200
    assertTemplateUsed(response, "posts/confirm_delete.html")


@pytest.mark.django_db
def test_PostDeleteView_delete_post(create_test_post, client):
    """
    Test if Post object gets deleted successfully through a POST request
    """

    # User object comes from create_test_post fixture
    client.force_login(user=User.objects.get(username="user"))

    post_id = Post.objects.all().first().id

    response = client.post(f"/posts/{post_id}/delete/")

    assert response.status_code == 302
    assert len(Post.objects.all()) == 0


@pytest.mark.django_db
def test_PostDeleteView_check_message(create_test_user, create_test_post, client):
    """
    Test if message sent by the view is right
    """
    client.force_login(user=create_test_user)
    post_id = Post.objects.all().first().id
    client.post(f"/posts/{post_id}/delete/")
    response = client.get("/posts/")

    # &#x27 means the ' symbol
    assert b"You aren&#x27;t allowed to delete this post" in response.content

    client.force_login(user=User.objects.get(username="user"))
    post_id = Post.objects.all().first().id
    client.post(f"/posts/{post_id}/delete/")
    response = client.get("/posts/")

    assert b"Post deleted successfully!" in response.content


# CommentDeleteView


@pytest.mark.django_db
def test_CommentDeleteView_delete_comment(
    create_test_user,
    create_test_comment,
    client,
):
    """
    Test if Comment object gets deleted successfully through a POST request
    """

    # User object comes from create_test_comment fixture
    client.force_login(user=User.objects.get(username="user"))

    comment_id = Comment.objects.all().first().id

    response = client.post(f"/posts/comments/{comment_id}/delete/")

    assert response.status_code == 302
    assert len(Comment.objects.all()) == 0


@pytest.mark.django_db
def test_CommentDeleteView_check_message(create_test_user, create_test_comment, client):
    """
    Test if message sent by the view is right
    """
    client.force_login(user=create_test_user)
    comment_id = Comment.objects.all().first().id
    client.post(f"/posts/comments/{comment_id}/delete/")
    response = client.get("/posts/")

    # &#x27 means the ' symbol
    assert b"You aren&#x27;t allowed to delete this comment" in response.content

    client.force_login(user=User.objects.get(username="user"))
    comment_id = Comment.objects.all().first().id
    client.post(f"/posts/comments/{comment_id}/delete/")
    response = client.get("/posts/")

    assert b"Comment deleted successfully!" in response.content


# PostUpdateView


@pytest.mark.django_db
def test_PostUpdateView_template_used(create_test_user, create_test_post, client):
    """
    Test if the right template is used in view
    """
    client.force_login(user=create_test_user)

    post_id = Post.objects.all().first().id

    response = client.get(f"/posts/{post_id}/update/")

    assert response.status_code == 200
    assertTemplateUsed(response, "posts/update.html")


@pytest.mark.django_db
def test_PostUpdateView_update_post(create_test_post, client):
    """
    Test if Post object gets updated successfully through a POST request
    """

    # User object comes from create_test_post fixture
    client.force_login(user=User.objects.get(username="user"))

    post_id = Post.objects.all().first().id

    data = {
        "content": "new post content",
    }

    response = client.post(f"/posts/{post_id}/update/", data=data)

    assert response.status_code == 302
    assert Post.objects.all().first().content == "new post content"


@pytest.mark.django_db
def test_PostUpdateView_check_message(create_test_user, create_test_post, client):
    """
    Test if message sent by the view is right
    """
    client.force_login(user=create_test_user)
    post_id = Post.objects.all().first().id
    client.post(f"/posts/{post_id}/update/", data={"content": "new post content"})
    response = client.get("/posts/")

    # &#x27 means the ' symbol
    assert b"You aren&#x27;t allowed to update this post" in response.content

    client.force_login(user=User.objects.get(username="user"))
    post_id = Post.objects.all().first().id
    client.post(f"/posts/{post_id}/update/", data={"content": "new post content"})
    response = client.get("/posts/")

    assert b"Post updated successfully!" in response.content
