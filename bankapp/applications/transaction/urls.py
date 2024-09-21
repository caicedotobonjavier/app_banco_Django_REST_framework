from django.urls import path
#
from . import views
#
app_name = 'transaction_app'

urlpatterns = [
    path('transaction', views.TransactionView.as_view(), name='transaction'),
    path('search-balance', views.SearchBalanceView.as_view(), name='search'),
    path('search-operations', views.OperationsUserView.as_view(), name='search_operations'),
]