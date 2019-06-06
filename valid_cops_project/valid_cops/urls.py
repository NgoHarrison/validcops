from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='valid-home'),
    path('base', views.base, name='valid-base'),
]