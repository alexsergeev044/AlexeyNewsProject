from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
   NewsList, NewsSearch, NewsDetail,
   NewsCreate, NewsEdit, NewsDelete,
   ArticlesCreate, ArticlesEdit, ArticlesDelete,
   subscriptions
)

urlpatterns = [
   path('', NewsList.as_view(), name='post_list'),
   path('news/', NewsList.as_view(), name='news_list'),
   path('articles/', cache_page(60*1)(NewsList.as_view()), name='articles_list'),
   path('news/<int:pk>', NewsDetail.as_view(), name='post_detail'),
   path('news/search/', NewsSearch.as_view(), name='post_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', ArticlesEdit.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]