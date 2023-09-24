from django.urls import path

from .views import NewsList, ShowNews

app_name = 'news'

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('post/<int:pk>/', ShowNews.as_view(), name='post')
]