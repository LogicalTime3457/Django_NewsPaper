from datetime import datetime
import pytz

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (
    View, ListView, DetailView, CreateView, UpdateView, DeleteView
)

from django.core.cache import cache
from django.utils import timezone


from .models import Post, Category
from .filters import PostFilter
from .forms import PostForms
from .tasks import notify_about_new_post, mailing_weekly


class NewsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_create'] = Post.dateCreation
        context['next_new'] = None
        return context



    # def get(self, request):
    #     string = _('All News')
    #
    #     return HttpResponse(string)


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'new'

#здесь мы применим кэширование (при иизменении новости)
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'news-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)

        return obj


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
    template_names = 'flatpages//post_edit.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForms
    model = Post
    template_name = 'flatpages/post_update.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'flatpages/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['postCategory'] = self.postCategory
        return context


@login_required
def add_subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = f"Вы успешно подписались на рассылку новостей категории: '{category}'"
    return render(request, 'flatpages/subscribe.html', {'message': message, })


@login_required
def off_subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = f"Вы успешно отписались от рассылки новостей категории: '{category}'"
    return render(request, 'flatpages/offsubscribe.html', {'message': message, })


class WeekView(View):
    def get(self, request):
        notify_about_new_post.delay()
        return redirect("/")


class WeekViews(View):
    def get(self, request):
        mailing_weekly.delay()
        return redirect("/")


class Index(View):
    def get(self, request):

        current_time = timezone.now()

        context = {
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones,  # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'default.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')






