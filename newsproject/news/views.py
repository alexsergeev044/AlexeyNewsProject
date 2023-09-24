from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post


class NewsList(ListView):
    model = Post
    ordering = ['-post_date']
    template_name = 'news.html'
    context_object_name = 'newslist'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset


class ShowNews(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'