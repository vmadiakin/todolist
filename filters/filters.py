import django_filters
from django.db import models
from goals.models import Goal


class GoalDateFilter(django_filters.FilterSet):
    due_date = django_filters.DateFromToRangeFilter(field_name="due_date", lookup_expr="range")

    class Meta:
        model = Goal
        fields = {
            "due_date": ["gte", "lte"],
            "category": ["exact", "in"],
            "status": ["exact", "in"],
            "priority": ["exact", "in"],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["due_date"].widget.widgets[0].attrs["placeholder"] = "С"
        self.filters["due_date"].widget.widgets[1].attrs["placeholder"] = "ДО"
