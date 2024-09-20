from django.urls import path
#
from . import views
#
app_name = 'operation_app'

urlpatterns = [
    path('add-operation', views.AddOperationView.as_view(), name='add'),
]