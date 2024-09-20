from django.urls import path, re_path, include
#
from . import views

app_name = 'account_app'

urlpatterns = [
    path('create-account', views.AccountView.as_view(), name='create')
]
