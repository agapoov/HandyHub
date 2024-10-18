from django.urls import path

from orders.views import OrderActionView

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registration/', views.register_view, name='registration'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('@<str:username>/', views.PublicUserProfileView.as_view(), name='public_profile'),
    path('orders/<int:pk>/<str:action>/', OrderActionView.as_view(), name='order-action'),
    path('transactions/', views.TransactionHistoryView.as_view(), name='transactions'),
    path('logout/', views.logout_view, name='logout')
]
