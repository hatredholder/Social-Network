from django import forms

from .models import Message, Profile


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "bio", "avatar")


class MessageModelForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Send a message.."}),
    )

    class Meta:
        model = Message
        fields = ("content",)
