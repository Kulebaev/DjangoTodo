# authentication/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('add_city/', views.add_city, name='add_city'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_selected_tasks/', views.delete_selected_tasks, name='delete_selected_tasks'),
    path('complete_selected_tasks/', views.complete_selected_tasks, name='complete_selected_tasks'),
]
