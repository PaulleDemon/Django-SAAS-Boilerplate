from django import forms
from .models import Blog, BlogImage


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'body']


class BlogImageForm(forms.ModelForm):

    class Meta:
        model = BlogImage
        fields = '__all__'