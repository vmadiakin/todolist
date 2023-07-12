from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from core.models import User


class GoalCategory(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)


class Status(models.IntegerChoices):
    TO_DO = 1, "К выполнению"
    IN_PROGRESS = 2, "В процессе"
    DONE = 3, "Выполнено"
    ARCHIVED = 4, "Архив"


class Priority(models.IntegerChoices):
    LOW = 1, "Низкий"
    MEDIUM = 2, "Средний"
    HIGH = 3, "Высокий"
    CRITICAL = 4, "Критический"


class Goal(models.Model):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="Заголовок", max_length=255, validators=[MinLengthValidator(1)])
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT, related_name="goals")
    created = models.DateTimeField(verbose_name="Дата создания", default=timezone.now, editable=False)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True, editable=False)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    due_date = models.DateField(verbose_name="Дата выполнения", null=True, blank=True)
    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=Status.choices, default=Status.TO_DO)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет", choices=Priority.choices, default=Priority.MEDIUM)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.PROTECT, related_name="goals")

    def __str__(self):
        return self.title
