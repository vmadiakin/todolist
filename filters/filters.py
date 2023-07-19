import django_filters
from goals.models import Goal


class GoalDateFilter(django_filters.FilterSet):
    due_date = django_filters.DateFromToRangeFilter(
        field_name="due_date",
        lookup_expr=("gte", "lte"),
    )
    category = django_filters.CharFilter(lookup_expr='exact')
    status = django_filters.NumberFilter(lookup_expr='exact')
    priority = django_filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = Goal
        fields = {
            "due_date": ["range"],
            "category": ["exact", "in"],
            "status": ["exact", "in"],
            "priority": ["exact", "in"],
        }