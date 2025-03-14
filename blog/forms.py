from django import forms
from .models import Post, Tag

class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ['title', 'content','slug','author', 'categories', 'tags', 'image', 'is_published']