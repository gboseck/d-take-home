from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/create/', views.create_user),
    path('posts/create/', views.create_post),
    path('users/top/', views.top_posts),
    path('users/follow/', views.follow_user)
    # Add remaining endpoints here
]
