import django_filters
from django.db import models
from goals.models import Goal


class GoalDateFilter(django_filters.FilterSet):
    due_date = django_filters.DateFromToFilter()
    category = django_filters.CharFilter(lookup_expr='exact')
    status = django_filters.NumberFilter(lookup_expr='exact')
    priority = django_filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = Goal
        fields = {
            "due_date": ["lte", "gte"],
            "category": ["exact", "in"],
            "status": ["exact", "in"],
            "priority": ["exact", "in"],
        }

    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }