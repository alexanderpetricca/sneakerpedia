from django.urls import path

from sneakers import views


urlpatterns = [
    path('', views.home_page_view, name='home')
]