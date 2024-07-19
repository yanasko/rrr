from django.contrib import admin
from .models import Category, Post,  Comment,PostCategory, Author
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


admin.site.register(Category)
#admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(PostCategory)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

