from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_create'] = Post.dateCreation
        context['next_new'] = None
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'new'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_create'] = Post.dateCreation
        context['next_new'] = None
        return context