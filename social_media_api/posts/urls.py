# from django.urls import path
# from .views import post_list_create, view_post_details, comment_list_create

# urlpatterns = [
#     path('posts/', post_list_create, name='post-list-create'),
#     path('posts/<int:pk>/', view_post_details, name='post-detail'),
#     path('posts/<int:post_id>/comments/', comment_list_create, name='comment-list-create'),
# ]

from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, user_feed



router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    #router URL definition
    path('', include(router.urls)),
    #User Feed URL definition
    path('feed/', user_feed, name='user-feed'),

     
    # Post URLs
    path('posts/', views.view_all_posts, name='view-all-posts'),
    path('posts/<int:pk>/', views.view_post_details, name='view-post-details'),
    path('posts/create/', views.create_post, name='create-post'),
    path('posts/<int:pk>/update/', views.update_post, name='update-post'),
    path('posts/<int:pk>/delete/', views.delete_post, name='delete-post'),
    
    # Comment URLs
    path('posts/<int:post_pk>/comments/', views.view_all_comments, name='comment-list'),
    path('posts/<int:post_pk>/comments/create/', views.create_comment, name='create-comment'),
    path('comments/<int:pk>/update/', views.update_comment, name='update-comment'),
    path('comments/<int:pk>/delete/', views.delete_comment, name='delete-comment'),
    
    #Like and Unlike URLs
    path('<int:pk>/like/', views.like_post, name='like_post'),
    path('<int:pk>/unlike/', views.unlike_post, name='unlike_post'),
]