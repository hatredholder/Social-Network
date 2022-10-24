def get_list_of_profiles_by_user(users):
    result = []

    for user in users:
        # Import inside fuction to avoid circular import
        from .models import Profile

        result.append(Profile.objects.get(user=user))

    return result


def get_likes_received_count(posts):
    # Get all Profile's posts,
    # get users who liked it,
    # count users
    total_liked = 0
    for post in posts:
        total_liked += post.liked.all().count()

    return total_liked
