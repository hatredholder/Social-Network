from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .forms import MessageModelForm, ProfileModelForm
from .models import Message, Profile, Relationship


@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False
    posts = profile.get_all_authors_posts()
    len_posts = True if len(profile.get_all_authors_posts()) > 0 else False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
            
    context = {
        'profile':profile,
        'form':form,
        'confirm':confirm,
        'posts':posts,
        'len_posts':len_posts,
    }

    return render(request, 'profiles/my_profile.html', context)

@login_required
def received_invites_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True
    context = {
        'qs':results,
        'is_empty':is_empty,
    }
    return render(request, 'profiles/received_invites.html', context)

@login_required
def sent_invites_view(request):
    user = request.user
    qs = Profile.objects.get_all_sent_invites(user)
    context = {
        'qs':qs
    }

    return render(request, 'profiles/sent_invites_list.html', context)

def follow_unfollow_user(request):
    if request.method == 'POST':
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('posts:main-post-view')

@login_required
def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'sent':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')

@login_required
def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')

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
    user = request.user
    profile = Profile.objects.get(user=user)
    qs = Profile.objects.get_my_friends_profiles(user)
    
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

def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='sent')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')

@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) or (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')
