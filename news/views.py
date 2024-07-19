from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, View)
from .models import Post, Category, Comment, Author
from .filter import PostFilter
from .forms import PostForm, CommentForm #AuthorForm
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.mixins import PermissionRequiredMixin
from .tasks import crazy


class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    #model = Post
    # Поле, которое будет использоваться для сортировки объектов
    #ordering = 'title'
    queryset = Post.objects.all()
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к спискуexit объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10


class PostSearch(ListView):
    model = Post
    ordering = '-some_datetime'
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CommentCreate(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comment_create.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.post_id = self.kwargs['pk']
        comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs['pk']
        return context


class PostDetail(CommentCreate, DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    context_object_name = 'create'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles/create':
            post.post_news = 'AR'
        post.save()
        crazy.delay(form.instance.pk)
        return super().form_valid(form)


def home_page(request):
    # получаем все значения модели
    data = Post.objects.all()
    return render(request, 'page.html', {'data': data})


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'edit'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    #context_object_name = 'delete'
    success_url = reverse_lazy('post_list')


class Posts(View):
    def get(self, request):
        posts = Post.objects.order_by('-rating')
        p = Paginator(posts, 1)
        posts = p.get_page(request.GET.get('page', 1))
        data = {
            'posts': posts,
        }
        return render(request, 'post/search.html', data)


class CategoryList(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category,
                                          id=self.kwargs['pk']
                                          )
        queryset = Post.objects.filter(category=self.category).order_by('-some_datetime')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        context['news'] = Post.objects.all()
        return context

@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = "Теперь вы подписаны на категорию"
    return render(request, 'subscribe.html', {'category': category, 'message': message})


# class CreateAuthor(CreateView):
    # form_class = AuthorForm
    # model = Author
    # template_name = 'author_create.html'
    #
    # def form_valid(self, form):
    #     author = form.save(commit=False)
    #     author.user = self.request.user
    #     author.post_id = self.kwargs['pk']
    #     author.save()
    #     return super().form_valid(form)
    # #
    # # def get_context_data(self, **kwargs):
    # #     context = super().get_context_data(**kwargs)
    # #     context['post_id'] = self.kwargs['pk']
    # #     return context




# class CommentDetail(DetailView):
#     model = Comment
#     template_name = 'comment.html'
#     context_object_name = 'comment'

