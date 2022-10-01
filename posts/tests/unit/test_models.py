from posts.models import Post

from django.contrib.auth.models import User

from profiles.models import Profile

import pytest


# Post model tests


@pytest.mark.django_db
def test_post_model_is_created(create_test_post):
    """
    Test if the post model is being successfully created
    """
    assert len(Post.objects.all()) == 1
    

@pytest.mark.django_db
def test_post_model_str_method(create_empty_profile):
    """
    Test if the post model str method is working as intended
    """
    post_short_content = Post.objects.create(
        content="short content",
        author=create_empty_profile,
    )
    post_long_content = Post.objects.create(
        content="long content long content long content long content long content long content",
        author=create_empty_profile,
    )

    assert str(post_short_content) == "testuser - short content"
    assert (
        str(post_long_content) == "testuser - long content long content long content long conten.."
    )


@pytest.mark.django_db
def test_post_model_num_comments_method(create_test_post):
    """
    Test if the post model str num comments is working as intended
    """
    post = create_test_post
    assert post.num_comments() == 0


@pytest.mark.django_db
def test_post_model_manager_get_related_posts_method(create_profile_with_friends_followings):
    """
    Test if post model manager get related posts method works correctly
    """

    # Create a post of user our profile follows
    # (user comes from the fixture)
    Post.objects.create(
        content="following content",
        author=Profile.objects.get(user=User.objects.get(username="testuser")),
    )

    # Create a post of user's friend
    # (user comes from the fixture)
    Post.objects.create(
        content="following content",
        author=Profile.objects.get(user=User.objects.get(username="frienduser")),
    )

    # Check if get_related_posts returns 2 posts
    assert len(
        Post.objects.get_related_posts(user=create_profile_with_friends_followings.user)
    ) == 2

