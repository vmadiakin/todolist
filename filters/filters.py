import django_filters
from django.db import models
from goals.models import Goal


class DateFromToRangeFilter(django_filters.DateFromToRangeFilter):
    def filter(self, qs, value):
        if value and value.start:
            qs = qs.filter(**{'{}__gte'.format(self.field_name): value.start})
        if value and value.stop:
            qs = qs.filter(**{'{}__lte'.format(self.field_name): value.stop})
        return qs


class GoalDateFilter(django_filters.FilterSet):
    due_date = DateFromToRangeFilter()
    category = django_filters.CharFilter(lookup_expr='exact')
    status = django_filters.NumberFilter(lookup_expr='exact')
    priority = django_filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = Goal
        fields = {
            "due_date": ["gte", "lte"],
            "category": ["exact", "in"],
            "status": ["exact", "in"],
            "priority": ["exact", "in"],
        }

    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }
