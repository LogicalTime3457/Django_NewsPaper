import django_filters
from django_filters import FilterSet
from django.forms import DateInput

from .models import Post, Author, Category


class PostFilter(FilterSet):

    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title',
    )

    category = django_filters.ModelMultipleChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Category',
    )

    dateCreation = django_filters.DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Date',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'},
        ),
    )

    author = django_filters.ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Author',
        empty_label='Select a author',
    )


