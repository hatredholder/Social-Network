from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .forms import MessageModelForm, ProfileModelForm
from .models import Message, Profile, Relationship
from .views_utils import (follow_unfollow, get_profile_by_pk,
                          get_received_invites, get_request_user_profile,
                          get_sent_invites, redirect_back)


@login_required
def my_profile_view(request):
    """
    Shows request's user profile.
    View url: /profiles/myprofile
    """
    profile = get_request_user_profile(request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    
    posts = profile.get_all_authors_posts()
    len_posts = len(profile.get_all_authors_posts())

    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
            
    context = {
        'profile':profile,
        'form':form,
        'posts':posts,
        'len_posts':len_posts,
        'confirm':confirm,
    }

    return render(request, 'profiles/my_profile.html', context)

@login_required
def received_invites_view(request):
    """
    Shows request's user received invites.
    View url: /profiles/received_invites
    """
    profile = get_request_user_profile(request.user)
    qs = get_received_invites(profile)
    
    is_empty = False

    if not len(qs):
        is_empty = True

    context = {
        'qs':qs,
        'is_empty':is_empty,
    }

    return render(request, 'profiles/received_invites.html', context)

@login_required
def sent_invites_view(request):
    """
    Shows request's user sent invites.
    View url: /profiles/sent_invites
    """
    profile = get_request_user_profile(request.user)
    qs = get_sent_invites(profile)

    is_empty = False

    if not len(qs):
        is_empty = True

    context = {
        'qs':qs,
        'is_empty':is_empty,
    }

    return render(request, 'profiles/sent_invites.html', context)

@login_required
def switch_follow_user(request):
    """
    Follows/unfollows user by pk.
    View url: /profiles/switch_follow
    """
    if request.method == 'POST':
        my_profile = get_request_user_profile(request.user)
        profile = get_profile_by_pk(request)

        follow_unfollow(my_profile, profile)

    return redirect_back(request)

@login_required
def accept_invitation(request):
    """
    Accepts invitation from user by pk.
    View url: /received_invites/accept
    """
    if request.method == 'POST':
        sender = get_profile_by_pk(request)
        receiver = get_request_user_profile(request.user)

        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if rel.status == 'sent':
            rel.status = 'accepted'
            rel.save()
            
    return redirect_back(request)

@login_required
def reject_invitation(request):
    """
    Rejects (deletes) invitation from user by pk.
    View url: /received_invites/reject
    """
    if request.method == 'POST':
        sender = get_profile_by_pk(request)
        receiver = get_request_user_profile(request.user)

        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)

        if rel.status == 'sent':
            rel.delete()

    return redirect_back(request)

@login_required
def profile_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {
        'qs':qs
    }

    return render(request, 'profiles/profile_list.html', context)

@login_required
def my_friends_view(request):
    profile = get_request_user_profile(request.user)
    qs = Profile.objects.get_my_friends_profiles(request.user)
    
    context = {
        'qs':qs,
        'following':profile.following.all()
    }

    return render(request, 'profiles/my_friends.html', context)

@login_required
def search_profiles(request):
    if request.method == 'POST':
        search = request.POST['search']
        profiles = Profile.objects.filter(user__username__contains=search)
        if search:
            return render(request, 'profiles/search_profiles.html', {'search':search, 'profiles':profiles})
    return render(request, 'profiles/search_profiles.html')

@login_required
def send_invitation(request):
    if request.method == 'POST':
        sender = get_request_user_profile(request.user)
        receiver = get_profile_by_pk(request)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='sent')

        return redirect_back(request)
    return redirect('profiles:my-profile-view')

@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        sender = get_request_user_profile(request.user)
        receiver = get_profile_by_pk(request)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) or (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect_back(request)
    return redirect('profiles:my-profile-view')

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    
    def get(self, request, *args, **kwargs):
        if Profile.objects.get(user=self.request.user) == self.get_object():
            return redirect("profiles:my-profile-view")
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)

        following = profile.following.all

        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.receiver.user)
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        context['following'] = following
        return context  

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)

        following = profile.following.all
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.receiver.user)
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        context['following'] = following
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context

class MessengerListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/messenger.html'

    def get_queryset(self):
        qs = Profile.objects.get(user=self.request.user)
        return qs.friends.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context

class ChatMessageView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'profiles/chat.html'
    form_class = MessageModelForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.sender = Profile.objects.get(user=self.request.user)
            instance.receiver = self.get_object()
            instance.save()
            return redirect(f"http://127.0.0.1:8000/profiles/chat/{self.kwargs.get('pk')}/")
        else:
            return redirect(f"http://127.0.0.1:8000/profiles/chat/{self.kwargs.get('pk')}/")

    def get_object(self):
        pk = self.kwargs.get("pk")
        profile = Profile.objects.get(pk=pk)
        return profile


    def get_queryset(self):
        sent = Message.objects.filter(sender=Profile.objects.get(user=self.request.user), receiver=self.get_object())
        received = Message.objects.filter(sender=self.get_object(), receiver=Profile.objects.get(user=self.request.user))
        messages = sent | received
        ordered_messages = list(messages.order_by('-created').values_list('content', flat=True))

        return(ordered_messages)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = self.get_object()
        context['form'] = self.form_class
        context['is_empty'] = False
        context['qs'] = self.get_queryset()
        context['received'] = list(Message.objects.filter(sender=self.get_object(), receiver=Profile.objects.get(user=self.request.user)).values_list('content', flat=True))
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context
