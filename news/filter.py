from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    some_datetime = DateFilter(
        field_name='some_datetime',
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='time__gte',
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            #'author': ['exact'],
            #'author': ['icontains'],
            #'some_datetime': ['gt']
            'category': ['exact'],
        }


