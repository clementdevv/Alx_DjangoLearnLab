from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    path('comment/<int:pk>/', post_detail, name='post_detail'),
    path('comment/<int:pk>/update/', edit_comment, name='update_comment'),
    path('comment/<int:pk>/delete/', delete_comment, name='delete_comment'),
    
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('search/', search_posts, name='search_posts'),
    path('tags/<str:tag_name>/', posts_by_tag, name='posts_by_tag'),
    
]
















# ["post/<int:pk>/comments/new/"]
# ["tags/<slug:tag_slug>/", "PostByTagListView.as_view()"]