# Generated by Django 4.2.2 on 2023-07-21 03:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(1)], verbose_name='Заголовок')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Дата выполнения')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'К выполнению'), (2, 'В процессе'), (3, 'Выполнено'), (4, 'Архив')], default=1, verbose_name='Статус')),
                ('priority', models.PositiveSmallIntegerField(choices=[(1, 'Низкий'), (2, 'Средний'), (3, 'Высокий'), (4, 'Критический')], default=2, verbose_name='Приоритет')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='goals', to='goals.goalcategory', verbose_name='Категория')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='goals', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Цель',
                'verbose_name_plural': 'Цели',
            },
        ),
    ]
