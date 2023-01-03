from django.urls import path

from .views import (
    NewsList, NewsDetail, NewsSearch, PostCreate,
    PostUpdate, PostDelete, CategoryListView, add_subscribe, off_subscribe,
)

urlpatterns = [
    path('', NewsList.as_view(), name='post_list'),
    path('<int:pk>', NewsDetail.as_view(), name='post_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', add_subscribe, name='subscribe'),
    path('categories/<int:pk>/offsubscribe', off_subscribe, name='offsubscribe'),
]