from django.contrib import admin
from django.urls import path
from account import views


urlpatterns = [
    path('user', views.UserView.as_view(), name='users'),
    path('login', views.Login, name='api-token-auth'),
    # path('verify', views.OtpVerify.as_view(), name='verify'),
    # path('activate/<uidb64>/<token>',activate,name='activate'),
]
