from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView, UpdateView
from profiles.models import Profile
from profiles.views_utils import get_request_user_profile, redirect_back

from .forms import CommentModelForm, PostModelForm, PostUpdateModelForm
from .models import Comment, Post
from .views_utils import (add_comment_if_submitted, add_post_if_submitted,
                          get_post_id_and_post_obj, like_unlike_post, get_post_by_pk)


@login_required
def post_comment_create_and_list_view(request):
    """
    Shows request's user friends.
    View url: /posts/
    """
    qs = Post.objects.get_friends_posts(user=request.user)
    profile = get_request_user_profile(request.user)

    p_form = PostModelForm()
    c_form = CommentModelForm()

    if add_post_if_submitted(request, profile):
        return redirect_back(request)

    if add_comment_if_submitted(request, profile):
        return redirect_back(request)

    context = {
        'qs':qs,
        'profile':profile,

        'p_form':p_form,
        'c_form':c_form,
    }
    
    return render(request, 'posts/main.html', context)

@login_required
def switch_like(request):
    """
    Adds/removes like to a post.
    View url: /posts/like/
    """
    if request.method == 'POST':
        post_id, post_obj = get_post_id_and_post_obj(request)
        profile = get_request_user_profile(request.user)

        like_unlike_post(profile, post_id, post_obj)

    return redirect_back(request)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deletes a post by pk.
    View url: /posts/<pk>/delete/
    """
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('posts:main-post-view')

    def get_object(self, *args, **kwargs):
        post = get_post_by_pk(self.kwargs)   
        return post

    def form_valid(self, *args, **kwargs):
        success_url = self.get_success_url()
        post = get_post_by_pk(self.kwargs)
        
        # If post's author doesnt equal request's user
        if post.author.user != self.request.user:
            messages.add_message(self.request, messages.ERROR, 'You aren\'t allowed to delete this post')
            return HttpResponseRedirect(success_url)
        
        # Executes only if post's author user
        # and request's user are the same
        self.object.delete()
        messages.add_message(self.request, messages.SUCCESS, 'Post deleted successfully!')
        return HttpResponseRedirect(success_url)

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('posts:main-post-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Comment.objects.get(pk=pk)
        if not obj.user.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the comment to be able to delete it')
        return obj

class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostUpdateModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main-post-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You need to be the author of the post to be able to delete it')
            return super().form_invalid(form)
