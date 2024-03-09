from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminView, name='admin_page'),
    path('<int:pk>', views.deleteVIO, name='delete'),
    path('room/<int:room>/', views.filterByRoom, name='filRoom'),
    path('?query=<int:room>/', views.filterByRoom, name='filRoom'),
    path('data/<str:date>/', views.filterByDate, name='filDate'),
    path('soop/<str:soop_fio>/', views.filterBySoop_fio, name='filSoop_fio')
]