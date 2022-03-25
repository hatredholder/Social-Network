from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile


class PostManager(models.Manager):

    def get_friends_posts(self, user):
        my_profile = Profile.objects.get(user=user)
        qs = my_profile.friends.all()

        profiles = set([])

        result = []
        result.append(my_profile.posts.all())

        return_result = []

        for user_ in qs:
            profiles.add(Profile.objects.get(user=user_))

        for profile in profiles:
            result.append(profile.posts.all())
        
        for queryset in result:
            for post in queryset:
                return_result.append(post.pk)

        final = Post.objects.filter(pk__in=return_result).order_by("-created")
        return final

class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return str(self.content[:20])
    
    def num_comments(self):
        return self.comment_set.all().count()
        
    class Meta:
        ordering = ('-created', )

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"