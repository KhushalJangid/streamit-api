from django.contrib import admin
from django.urls import path
from main import views


urlpatterns = [
    path('courses', views.Courses.as_view()),
    path('mycourses/',views.purchased_courses),
    path('videos/list/<uuid:course_id>',views.list_videos),
    path('<uuid:course_id>/video/<uuid:video_id>',views.view_video),
]
