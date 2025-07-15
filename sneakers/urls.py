from django.urls import path

from sneakers import views


urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('query/', views.query_view, name='query'),
    path('sneaker/<str:pk>/', views.detail_view, name='detail')
]