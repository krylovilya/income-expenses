import datetime

import factory
from factory.fuzzy import FuzzyChoice

from apps.transactions.models import Category, Transaction, Widget
from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Factory класс для пользователя"""
    email = factory.Faker('email')
    username = factory.LazyAttribute(lambda el: el.email.split('@')[0])
    password = factory.Faker('password')

    class Meta:
        model = User


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory класс для категории"""
    title = factory.Faker('name')
    type = FuzzyChoice(Category.CategoryChoices.values)
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Category


class TransactionFactory(factory.django.DjangoModelFactory):
    """Factory класс для транзакции"""
    owner = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    amount = 100
    date = factory.Faker('date', end_datetime=datetime.date.today())

    class Meta:
        model = Transaction


class WidgetFactory(factory.django.DjangoModelFactory):
    """Factory класс для виджета"""
    owner = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    amount_limit = 200
    period = FuzzyChoice(Widget.PeriodChoices.values)
    criterion = FuzzyChoice(Widget.CriterionChoices.values)
    hex_color = factory.Faker('color')
    creation_date = factory.Faker('date', end_datetime=datetime.date.today())

    class Meta:
        model = Widget
