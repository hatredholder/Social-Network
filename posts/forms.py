from django import forms

from .models import Comment, Post


class PostCreateModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    
    class Meta:
        model = Post
        fields = ('content', 'image', )

class PostUpdateModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))

    class Meta:
        model = Post
        fields = ('content', )

class CommentCreateModelForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Add a comment..'}))

    class Meta:
        model = Comment
        fields = ('body', )
