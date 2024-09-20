from django.urls import path, re_path, include
#
from . import views

app_name = 'card_app'

urlpatterns = [
    path('add-card', views.AddCardView.as_view(), name='add')
]
