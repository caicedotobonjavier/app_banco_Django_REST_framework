from django.urls import path
#
from . import views
#
app_name = 'transaction_app'

urlpatterns = [
    path('transaction', views.TransactionView.as_view(), name='transaction')
]