from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Prefetch, Sum


class Category(models.Model):
    """Категория, имеет тип доход/расход"""

    class CategoryChoices(models.TextChoices):
        INCOME = 'IN', 'доход'
        EXPENSE = 'EX', 'расход'

    type = models.CharField(verbose_name='тип категории', choices=CategoryChoices.choices, max_length=2)
    title = models.CharField(verbose_name='название категории', max_length=128)
    owner = models.ForeignKey(to=get_user_model(), verbose_name='владелец категории', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} [{self.get_type_display()}]'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    @staticmethod
    def get_available_categories(owner, _filter):
        """Получить все категории текущего пользователя"""
        return Category.objects.filter(owner=owner).prefetch_related(
            Prefetch('transactions', queryset=_filter.qs))


class Transaction(models.Model):
    """Транзакция"""

    owner = models.ForeignKey(to=get_user_model(), verbose_name='владелец транзакции', on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, verbose_name='категория', on_delete=models.CASCADE,
                                 related_name='transactions')
    amount = models.IntegerField(verbose_name='сумма')
    date = models.DateField(auto_now_add=True, verbose_name='дата операции')

    def __str__(self):
        return f'{self.date} {self.category} {self.amount}'

    class Meta:
        verbose_name = 'транзакция'
        verbose_name_plural = 'транзакции'


class Widget(models.Model):
    """Виджет"""

    class PeriodChoices(models.IntegerChoices):
        DAY = 1, 'день'
        WEEK = 7, 'неделя'
        MONTH = 30, 'месяц'

    class CriterionChoices(models.TextChoices):
        MORE = '>', 'больше'
        LESS = '<', 'меньше'

    owner = models.ForeignKey(to=get_user_model(), verbose_name='владелец виджета', on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, verbose_name='категория виджета', on_delete=models.CASCADE,
                                 related_name='widgets')
    amount_limit = models.IntegerField(verbose_name='лимит суммы, которую можно потратить')
    period = models.IntegerField(verbose_name='срок действия', choices=PeriodChoices.choices)
    criterion = models.CharField(verbose_name='критерий (больше/меньше)',
                                 choices=CriterionChoices.choices, max_length=1)
    hex_color = models.CharField(verbose_name='цвет', default='#e5ff00', max_length=7)
    creation_date = models.DateField(auto_now_add=True, verbose_name='дата создания')

    def __str__(self):
        return self.category.title

    class Meta:
        verbose_name = 'виджет'
        verbose_name_plural = 'виджеты'

    @property
    def current_amount(self):
        return self.category.transactions.aggregate(Sum('amount'))['amount__sum'] or 0

    @property
    def deadline(self):
        return self.creation_date + timedelta(days=self.period)
