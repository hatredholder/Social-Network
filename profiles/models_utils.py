def find_likes_received_count(posts):
    # Get all Profile's posts, find users who liked it,
    # count users
    total_liked = 0        
    for post in posts:
        total_liked += post.liked.all().count()

    return total_liked