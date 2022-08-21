from .forms import CommentModelForm, PostModelForm
from .models import Post, Like


def add_post_if_submitted(request, profile):
    if 'submit_p_form' in request.POST:

        p_form = PostModelForm(request.POST, request.FILES)

        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()

            p_form = PostModelForm()    

            return True

def add_comment_if_submitted(request, profile):
    if 'submit_c_form' in request.POST:
        
        c_form = CommentModelForm(request.POST)

        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()

            c_form = CommentModelForm()

            return True

def get_post_id_and_post_obj(request):
    post_id = request.POST.get('post_id')
    post_obj = Post.objects.get(id=post_id)
    return post_id, post_obj

def like_unlike_post(profile, post_id, post_obj):

    # Remove / add target profile 
    # from liked field in post_obj
    if profile in post_obj.liked.all():
        post_obj.liked.remove(profile)
    else:
        post_obj.liked.add(profile)

    # Get Like object if post already liked, create Like object if not    
    like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

    # If Like object wasnt created - delete
    if not created:
        like.delete()
    # Else - save Like object
    else:
        like.value = 'Like'
        post_obj.save()
        like.save()