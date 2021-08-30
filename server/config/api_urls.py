from django.urls import include, path

urlpatterns = [
    path('users/', include('apps.users.urls.api_urls')),
    path('transactions/', include('apps.transactions.urls.api_urls')),
]
