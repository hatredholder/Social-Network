from profiles.models import Profile


def get_related_posts_queryset(profile, friends, following):
    """
    This function gets all profile's own posts, posts of users profile's friends,
    posts of users profile follows in a queryset.

    Here's how it works:

    1) We get all profiles of both his friends and of users he follows,
    we put them in a set so we dont have any duplicates

    2) We get querysets of both his own posts and posts of profiles
    we gathered in step 1 in a list

    3) Then, we get primary keys of each post in both of these querysets
    and put them in a list

    4) Lastly, we create a single queryset object using QuerySet API
    with those primary keys we gathered in step 3 and we order it by
    creation date (new first, old last)
    """
    # Importing inside function to avoid circular import
    from .models import Post

    unique_profiles = set()
    querysets = []
    post_pks = []

    # Get all profile's friend's profiles
    for user in friends:
        unique_profiles.add(Profile.objects.get(user=user))

    # Get all profiles of users, who profile follows
    for user in following:
        unique_profiles.add(Profile.objects.get(user=user))

    # Get querysets of all profile's own posts
    querysets.append(profile.posts.all())

    # Get querysets of all posts of each profile in unique_profiles
    for unique_profile in unique_profiles:
        querysets.append(unique_profile.posts.all())

    # Get post's primary keys of all post querysets
    for queryset in querysets:
        for post in queryset:
            post_pks.append(post.pk)

    # Finally, create one big queryset of all post's primary keys in post_pks
    result = Post.objects.filter(pk__in=post_pks).order_by("-created")
    return result
