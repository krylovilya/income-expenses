from rest_framework.routers import DefaultRouter

from apps.transactions.viewsets.viewsets import (CategoryViewSet,
                                                 TransactionViewSet,
                                                 WidgetViewSet)

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('transaction', TransactionViewSet, basename='transaction')
router.register('widget', WidgetViewSet, basename='widget')
