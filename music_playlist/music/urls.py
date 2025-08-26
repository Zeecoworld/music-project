from django.urls import path
from . import views

urlpatterns = [
    path('', views.music_list_view, name='music_list'),
    path('add/', views.add_music_view, name='add_music'),
]