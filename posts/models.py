from django.core.validators import FileExtensionValidator
from django.db import models

from profiles.models import Profile
from profiles.views_utils import get_request_user_profile

from .models_utils import get_related_posts_queryset


class PostManager(models.Manager):
    def get_related_posts(self, user):
        profile = get_request_user_profile(user)
        friends = profile.friends.all()
        following = profile.following.all()

        related_posts = get_related_posts_queryset(profile, friends, following)

        return related_posts


class Post(models.Model):
    """
    This model is used to show results in main.html
    """

    content = models.TextField()
    image = models.ImageField(
        blank=True,
        upload_to="posts",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg"])],
    )
    liked = models.ManyToManyField(Profile, blank=True, related_name="likes")
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        if len(str(self.content)) > 50:
            return f"{self.author} - {str(self.content)[:50].strip()}.."
        return f"{self.author} - {str(self.content)}"

    def num_comments(self):
        return self.comment_set.all().count()

    class Meta:
        ordering = ("-created",)


class Comment(models.Model):
    """
    This model is used in Posts for comments
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} - {self.content}"


class Like(models.Model):
    """
    This model is used to leave likes on Posts
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} liked {self.post}"
