from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Comment, Author


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['title', 'author', 'text',  'category', 'image']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if title == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )
        return

    widgets = {
        'image': forms.FileInput(),
    }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']


# class AuthorForm(forms.ModelForm):
#
#     class Meta:
#         model = Author
#         fields = ['user']








