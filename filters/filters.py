import django_filters
from django.db import models
from goals.models import Goal


class GoalDateFilter(django_filters.FilterSet):
    due_date = django_filters.DateFromToRangeFilter()

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
        self.filters["due_date"].lookup_expr = "range"  # Изменяем lookup_expr на "range"

        # Изменяем порядок полей "С" и "ДО" в форме фильтрации
        due_date_field = self.filters["due_date"].field
        due_date_field.widget.widgets[0].attrs["placeholder"] = "ДО"  # Изменяем placeholder для "ДО"
        due_date_field.widget.widgets[1].attrs["placeholder"] = "С"  # Изменяем placeholder для "С"
