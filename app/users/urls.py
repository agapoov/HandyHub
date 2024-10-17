from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registration/', views.register_view, name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.logout_view, name='logout')
]
