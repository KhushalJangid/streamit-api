from django.contrib import admin
from django.urls import path
from main import views


urlpatterns = [
    path('courses', views.list_courses),
    path('course/purchase/<uuid:course_id>', views.purchase_course),
    path('mycourses/',views.purchased_courses),
    path('wishlist/',views.whishlist),
    path('wishlist/add/<uuid:courseId>',views.add_to_whishlist),
    path('wishlist/remove/<uuid:courseId>',views.remove_from_whishlist),
    path('videos/list/<uuid:course_id>',views.list_videos),
    path('<uuid:course_id>/video/<uuid:video_id>',views.view_video),
]
