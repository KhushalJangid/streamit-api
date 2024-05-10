from django.contrib import admin
from django.urls import path
from api import views


urlpatterns = [
    path('post', views.Post.as_view()),
    path('inbox', views.Chat.as_view()),
]
