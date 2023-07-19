import django_filters
from goals.models import Goal


class GoalDateFilter(django_filters.FilterSet):
    due_date = django_filters.DateFromToRangeFilter(field_name="due_date")

    due_date__gte = django_filters.DateFilter(field_name="due_date", lookup_expr='gte')
    due_date__lte = django_filters.DateFilter(field_name="due_date", lookup_expr='lte')

    class Meta:
        model = Goal
        fields = {
            "due_date": ["exact"],
            "category": ["exact", "in"],
            "status": ["exact", "in"],
            "priority": ["exact", "in"],
        }
