from django.urls import path

from .views import (
    auth_views
)

urlpatterns = [
    path('login/', auth_views.LoginAPIView.as_view(), name='login'),
    path('register/', auth_views.RegisterAPIView.as_view(), name='register'),

]


