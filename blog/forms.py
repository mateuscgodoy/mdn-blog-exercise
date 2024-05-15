from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Blog, Comment


class CreateUserForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]


class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "content"]


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
