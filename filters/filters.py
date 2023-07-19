import django_filters
from django.db import models
from goals.models import Goal


class GoalDateFilter(django_filters.FilterSet):
    due_date__gte = django_filters.DateFilter(field_name='due_date', lookup_expr='gte')
    due_date__lte = django_filters.DateFilter(field_name='due_date', lookup_expr='lte')
    category = django_filters.CharFilter(lookup_expr='exact')
    status = django_filters.NumberFilter(lookup_expr='exact')
    priority = django_filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = Goal
        fields = {
            "category": ["exact", "in"],
            "status": ["exact", "in"],
            "priority": ["exact", "in"],
        }

    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['due_date__lte'].label = 'due_date__lte'
        self.filters['due_date__gte'].label = 'due_date__gte'
