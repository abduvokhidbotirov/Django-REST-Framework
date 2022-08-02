from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_home),
    path('create/', views.api_post),
    path('<int:pk>/', views.api_detail),
    path('edit/<int:pk>/', views.api_put),
    path('delete/<int:pk>/', views.api_delete),
    path('list-create/', views.api_list_create),
    path('api-rud/<int:pk>/', views.api_rud),
]