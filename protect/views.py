from django.shortcuts import render
from django.views.generic import ListView#TemplateView
from django.contrib.auth.mixins import  LoginRequiredMixin
from django_filters import FilterSet

from news.models import Comment, Post


class IndexView(LoginRequiredMixin, ListView): #TemplateView):
    model = Comment
    template_name = 'protect/index.html'
    context_object_name = 'comments'

    def get_queryset(self):
        queryset = Comment.objects.filter(post__author__user_id=self.request.user.id)
        self.filterset = PostFilter(self.request.GET,queryset, request=self.request.user.id)
        if self.request.GET:
            return self.filterset.qs
        return Comment.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #queryset = Comment.objects.filter(post__author__user_id=self.request.user.id)
        context['filterset'] = self.filterset #PostFilter(self.request.GET,queryset, request=self.request.user.id)
        return context
    #     context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
     #    return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostFilter(FilterSet):
    class Meta:
        model = Comment
        fields = [
            'post'
        ]

    def __init__(self, *args, **kwargs):
        super(PostFilter,self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(author__user_id=kwargs['request'])
