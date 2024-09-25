from django.urls import path
#
from . import views
#
app_name = 'transaction_app'

urlpatterns = [
    path('transaction', views.TransactionView.as_view(), name='transaction'),
    path('search-balance', views.SearchBalanceView.as_view(), name='search'),
    path('search-operations', views.OperationsUserView.as_view(), name='search_operations'),
    path('transaction-dates', views.TransactionByDate.as_view(), name='transaction_dates'),
    path('deposit-Withdraw-account', views.DepositWithdrawAccountView.as_view(), name='deposit'),
    path('virtual-pay', views.VirtualPayView.as_view(), name='virtual_pay'),
    path('detail-transactions', views.DetailTransactionView.as_view(), name='detail'),
]