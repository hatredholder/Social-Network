from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView

from profiles.views_utils import get_request_user_profile, redirect_back

from .forms import CommentCreateModelForm, PostCreateModelForm, PostUpdateModelForm
from .models import Comment, Post
from .views_utils import (
    add_comment_if_submitted,
    add_post_if_submitted,
    get_post_id_and_post_obj,
    like_unlike_post,
)


# Function-based views


@login_required
def post_comment_create_and_list_view(request):
    """
    Shows request's user friends.
    View url: /posts/
    """
    qs = Post.objects.get_related_posts(user=request.user)
    profile = get_request_user_profile(request.user)

    p_form = PostCreateModelForm()
    c_form = CommentCreateModelForm()

    if add_post_if_submitted(request, profile):
        return redirect_back(request)

    if add_comment_if_submitted(request, profile):
        return redirect_back(request)

    context = {
        "qs": qs,
        "profile": profile,
        "p_form": p_form,
        "c_form": c_form,
    }

    return render(request, "posts/main.html", context)


@login_required
def switch_like(request):
    """
    Adds/removes like to a post.
    View url: /posts/like/
    """
    if request.method == "POST":
        post_id, post_obj = get_post_id_and_post_obj(request)
        profile = get_request_user_profile(request.user)

        like_added = like_unlike_post(profile, post_id, post_obj)

    # Return JSON response for AJAX script in like.js
    return JsonResponse(
        {"total_likes": post_obj.liked.count(), "like_added": like_added},
    )


# Class-based views


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deletes a post by pk.
    View url: /posts/<pk>/delete/
    """

    model = Post
    template_name = "posts/confirm_delete.html"
    success_url = reverse_lazy("posts:main-post-view")

    def form_valid(self, *args, **kwargs):
        post = self.get_object()

        # If post's author user doesnt equal request's user
        if post.author.user != self.request.user:
            messages.add_message(
                self.request,
                messages.ERROR,
                "You aren't allowed to delete this post",
            )
            return HttpResponseRedirect(self.success_url)

        # Executes only if post's author user
        # and request's user are the same
        self.object.delete()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Post deleted successfully!",
        )
        return HttpResponseRedirect(self.success_url)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deletes a comment by pk.
    View url: /posts/comments/<pk>/delete/
    (This view is indentical to PostDeleteView)
    """

    model = Comment

    def form_valid(self, *args, **kwargs):
        comment = self.get_object()

        if comment.profile.user != self.request.user:
            messages.add_message(
                self.request,
                messages.ERROR,
                "You aren't allowed to delete this comment",
            )
            return redirect_back(self.request)

        # Delete the comment
        self.object.delete()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Comment deleted successfully!",
        )
        return redirect_back(self.request)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    Updates a post by pk.
    View url: /posts/<pk>/update/
    (This view is (again) indentical to PostDeleteView)
    """

    model = Post
    form_class = PostUpdateModelForm
    template_name = "posts/update.html"
    success_url = reverse_lazy("posts:main-post-view")

    def form_valid(self, form):
        profile = get_request_user_profile(self.request.user)

        if form.instance.author != profile:
            messages.add_message(
                self.request,
                messages.ERROR,
                "You aren't allowed to update this post",
            )
            return HttpResponseRedirect(self.success_url)

        # Update the post
        self.object = form.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Post updated successfully!",
        )
        return HttpResponseRedirect(self.success_url)
