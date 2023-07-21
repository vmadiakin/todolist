from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework import permissions, filters, generics, mixins
from rest_framework.pagination import LimitOffsetPagination
from filters.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, Status, Comment
from goals.serializers import GoalCategorySerializer, GoalSerializer, GoalCreateSerializer, CommentSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

        # Обновление статуса всех целей связанных с удаленной категорией
        goals = instance.goals.all()
        for goal in goals:
            goal.status = Status.ARCHIVED
            goal.save()

        return instance


class GoalCreateView(CreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoalListView(ListAPIView):
    serializer_class = GoalSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GoalDateFilter
    search_fields = ['title']
    ordering_fields = ['title', 'created']
    pagination_class = LimitOffsetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Goal.objects.filter(user=self.request.user)
        return queryset


class GoalAPIView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        return self.retrieve(request, pk=pk)

    def put(self, request, pk):
        return self.update(request, pk=pk)

    def patch(self, request, pk):
        return self.partial_update(request, pk=pk)

    def delete(self, request, pk):
        return self.destroy(request, pk=pk)


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        goal_id = self.request.GET.get('goal')
        print(goal_id)
        if goal_id is not None:
            try:
                goal = Goal.objects.get(pk=goal_id)
                serializer.save(user=self.request.user, goal=goal)
            except Goal.DoesNotExist:
                raise Http404("Цель с указанным идентификатором не найдена.")
        else:
            raise Http404("Параметр 'goal' должен быть указан в запросе.")


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Отфильтровать комментарии текущего пользователя
        return Comment.objects.filter(goal__user=self.request.user)


class CommentAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            return self.retrieve(request, pk=pk)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, pk):
        return self.update(request, pk=pk)

    def patch(self, request, pk):
        return self.partial_update(request, pk=pk)

    def delete(self, request, pk):
        return self.destroy(request, pk=pk)
