from .forms import PostModelForm, CommentModelForm
from .models import Post


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