from django.urls import path
#
from . import views
#
app_name = 'user_app'

urlpatterns = [
    path('create-user', views.AddUserVIew.as_view(), name='create'),
    path('login-user', views.LoginUserView.as_view(), name='login'),
    path('update-user', views.UpdateUserView.as_view(), name='update'),
    path('logout-user', views.LogoutUserView.as_view(), name='logout'),
    path('user-activate/<pk>/', views.ActivateUserView.as_view(), name='activate'),
    path('user-verify/<pk>/', views.VerifyLoginView.as_view(), name='verify'),
]