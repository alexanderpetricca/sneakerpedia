from django.urls import path

from sneakers import views


urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('query/', views.query_view, name='query'),
    path('sneaker/<str:pk>/', views.detail_view, name='detail'),
    
    path('manage/create-sneaker/', views.create_sneaker_view, name='create_sneaker'),
    path('manage/update-sneaker/<str:pk>/', views.update_sneaker_view, name='update_sneaker'),
    path('manage/delete-sneaker/<str:pk>/', views.delete_sneaker_view, name='delete_sneaker'),
]