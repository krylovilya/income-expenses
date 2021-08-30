from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

from apps.transactions.filters import (CategoriesDateFilter,
                                       TransactionDateFilter)
from apps.transactions.models import Category, Transaction
from apps.transactions.serializers.serializers import (
    AmountTransactionSerializer, SummaryCategorySerializer)


def summary_category(category):
    """Сумма транзакций категории"""
    return category.annotate(amount=Coalesce(Sum('transactions__amount', ), Value(0)))


def summary_categories(user, filter_data) -> list[dict[str, str, int]]:
    """Список категорий и сумма всех транзакций по каждой категории"""
    transaction_filter = TransactionDateFilter(data=filter_data, queryset=Transaction.objects.filter(owner=user))
    categories = Category.get_available_categories(user, transaction_filter)
    category_filter = CategoriesDateFilter(data=filter_data, queryset=categories)
    categories_with_amount = summary_category(category_filter.qs)
    serializer = SummaryCategorySerializer(categories_with_amount, many=True)
    return serializer.data


def amount_transactions(user, _filter):
    """Сумма всех доходов и расходов"""
    qs = _filter.qs
    income_summary = qs.filter(
        owner=user, category__type='IN').aggregate(Sum('amount'))["amount__sum"] or 0
    expense_summary = qs.filter(
        owner=user, category__type='EX').aggregate(Sum('amount'))["amount__sum"] or 0
    return AmountTransactionSerializer({
        'income_summary': income_summary,
        'expense_summary': expense_summary,
    }).data
