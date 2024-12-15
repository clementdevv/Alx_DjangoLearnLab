from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # Include fields that should be in the form

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content.strip():
            raise forms.ValidationError('Content cannot be empty')
        return content
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 5:
            raise forms.ValidationError("Content must be at least 5 characters long.")
        return content
    
    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        for tag in tags:
            if not Tag.objects.filter(name=tag.name).exists():
                Tag.objects.create(name=tag.name)
        return tags
    
    
    
#  ["TagWidget()", "widgets"]