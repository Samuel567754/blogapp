from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/new/', views.post_create, name='post-create'),
    path('post/<int:pk>/update/', views.post_update, name='post-update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
    path('category/<int:pk>/', views.category_posts, name='category-posts'),  # Category posts
    path('tags/<str:tag_name>/', views.tag_posts, name='tag-posts'),
]