from django.urls import path
# Импортируем созданное нами представление
from .views import (PostsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, CategoryList, subscribe, CommentCreate) #CreateAuthor
from django.views.decorators.cache import cache_page

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('post/', PostsList.as_view(), name='post_list'),
   path('post/search/', cache_page(60*1)(PostSearch.as_view())),
   path('post/<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
   path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('<int:pk>/comment/create', CommentCreate.as_view(), name='comment_create'),
   #path('author/create/', CreateAuthor.as_view(), name='author_create'),

]