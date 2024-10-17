from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:slug_url>/', views.CatalogView.as_view(), name='index'),
]