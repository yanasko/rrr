from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


news = "NE"
articles = "AR"

POST_TYPES = [
    (news, "Новоcти"),
    (articles, "Статьи")
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    # author = models.CharField(max_length=20, unique=True)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comm_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_comm_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'), 0))['pcr']

        self.rating = posts_rating*3+comm_rating+posts_comm_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)  # название категории
    subscribers = models.ManyToManyField(User, related_name='Подписчики')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_category(self):
        return self.name

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    some_datetime = models.DateTimeField(auto_now_add=True)   #автоматическая дата
    rating = models.IntegerField(default=0)
    post_type = models.CharField(max_length=2, choices=POST_TYPES)  # поле с выбором статья или новость
    #author = models.OneToOneField(Author, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    # def file_path(instance):
    #     return '/'.join(['image',instance.id])
    # image = models.ImageField(upload_to=file_path)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь 1 ко многим с моделью автор
    category = models.ManyToManyField(Category, through='PostCategory')  # связь многие ко многим с моделью категория ( с доп.моделью посткатегорией)

    def preview(self):
        sm_text = self.text[0:124] + '...'
        return sm_text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('post', args=[str(self.pk)])
    # def get_absolut_url(self):
    #     return f'/post/{self.pk}'


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Category;
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post;

    def __str__(self):
        return f'{self.post}: {self.category}'

    class Meta:
        verbose_name = 'Промежуточная модель PostCategory'
        verbose_name_plural = 'Промежуточная модель PostCategories'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post;
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
    text = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # def get_absolute_url(self):
    #     return reverse('post', args=[str(self.pk)])

    # def get_absolut_url(self):
    #     return f'/post/{self.pk}'
    def get_absolute_url(self):
        return reverse('comment_create')
