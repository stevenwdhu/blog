from . import views
from django.urls import path

app_name = 'userprofile'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete')
    ]