from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('add/', views.add, name='add'),
    path('random/', views.random, name='random'),
    path('wiki/<str:title>/', views.entry, name='entry'),
    path('wiki/<str:title>/edit/', views.edit, name='edit'),
    path('wiki/<str:title>/delete/', views.delete, name='delete'),
]
