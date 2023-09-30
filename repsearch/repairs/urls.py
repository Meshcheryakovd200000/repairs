from django.urls import path
from . import views

urlpatterns = [
    path('', views.repairs, name='repairs'),
    path('repair/<str:pk>/', views.repair, name='repair'),
    path('create-repair/', views.create_repair, name='create-repair'),
    path('update-repair/<str:pk>/', views.update_repair, name='update-repair'),
    path('delete-repair/<str:pk>/', views.delete_repair, name='delete-repair'),
]


























