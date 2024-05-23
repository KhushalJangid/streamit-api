from django.contrib import admin
from django.urls import path
from main import views


urlpatterns = [
    path('courses', views.Courses.as_view()),
    path('videos/list/<int:id>',views.list_videos)
]
