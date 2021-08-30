from rest_framework import serializers

from apps.transactions.models import Category, Transaction, Widget


class CategorySerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'owner', 'owner_username', 'type', 'title')
        read_only_fields = ('id', 'owner', 'owner_username')


class TransactionSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source='category.title', read_only=True)
    category_type = serializers.CharField(source='category.type', read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'owner', 'category', 'category_title', 'category_type', 'amount', 'date')
        read_only_fields = ('id', 'owner', 'category_title', 'category_type')


class AmountTransactionSerializer(serializers.Serializer):
    """Для подсчёта всех доходов и расходов"""

    income_summary = serializers.IntegerField(read_only=True)
    expense_summary = serializers.IntegerField(read_only=True)


class SummaryCategorySerializer(serializers.Serializer):
    """Для список категорий и суммы всех транзакций по каждой категории"""

    title = serializers.CharField(max_length=128, read_only=True)
    type = serializers.CharField(max_length=2, read_only=True)
    amount = serializers.IntegerField(read_only=True)


class WidgetSerializer(serializers.ModelSerializer):
    current_amount = serializers.ReadOnlyField()
    deadline = serializers.ReadOnlyField()

    class Meta:
        model = Widget
        fields = ('id', 'owner', 'category', 'amount_limit',
                  'period', 'criterion', 'hex_color',
                  'creation_date', 'current_amount', 'deadline')
