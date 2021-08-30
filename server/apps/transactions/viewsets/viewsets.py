from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.transactions.filters import (CategoriesDateFilter,
                                       TransactionDateFilter)
from apps.transactions.models import Category, Transaction, Widget
from apps.transactions.permissions import RequestUserIsObjectOwnerPermission
from apps.transactions.serializers.serializers import (CategorySerializer,
                                                       TransactionSerializer,
                                                       WidgetSerializer)
from apps.transactions.services import amount_transactions, summary_categories


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Create/List/Delete операции над категориями"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated & RequestUserIsObjectOwnerPermission,)
    filterset_class = CategoriesDateFilter
    filterset_fields = ('transactions__data',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        owner_queryset = self.queryset.filter(owner=self.request.user)
        return owner_queryset

    @action(detail=False)
    def get_summary_categories(self, request):
        """Список категорий и сумма всех транзакций по каждой категории"""
        user = request.user
        response_data = summary_categories(user, request.GET)
        return Response(response_data)


class TransactionViewSet(mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """Create/Update/List/Delete операции над транзакциями"""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated & RequestUserIsObjectOwnerPermission,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TransactionDateFilter
    filterset_fields = ('data',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        owner_queryset = self.queryset.filter(owner=self.request.user)
        return owner_queryset

    @action(detail=False)
    def get_amount_transactions(self, request):
        """Сумма всех доходов и расходов"""
        user = request.user
        _filter = TransactionDateFilter(data=request.GET, queryset=Transaction.objects.filter(owner=user))
        response_data = amount_transactions(request.user, _filter)
        return Response(response_data)


class WidgetViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Create/Delete/List операции над виджетами"""

    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    permission_classes = (permissions.IsAuthenticated & RequestUserIsObjectOwnerPermission,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        owner_queryset = self.queryset.filter(owner=self.request.user)
        return owner_queryset
