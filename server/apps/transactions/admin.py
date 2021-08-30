from django.contrib import admin

from apps.transactions.models import Category, Transaction, Widget


@admin.register(Category, Transaction, Widget)
class UserAdmin(admin.ModelAdmin):
    pass
