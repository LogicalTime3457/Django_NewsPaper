from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .models import Post
from .filters import PostFilter
from .forms import PostForms


class NewsList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_create'] = Post.dateCreation
        context['next_new'] = None
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'new'


class NewsSearch(ListView):
    model = Post
    template_name = 'flatpages/news_search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['filterset'] = self.filterset
       return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForms
    model = Post
    template_name = 'flatpages/post_edit.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForms
    model = Post
    template_name = 'flatpages/post_update.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('post_list')