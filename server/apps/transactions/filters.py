from django_filters import rest_framework as filters


class TransactionDateFilter(filters.FilterSet):
    """Фильтрация по датам, включая указанные даты для транзакция"""

    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')


class CategoriesDateFilter(filters.FilterSet):
    """Фильтрация по датам, включая указанные даты для категорий"""

    start_date = filters.DateFilter(field_name='transactions__date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='transactions__date', lookup_expr='lte')
