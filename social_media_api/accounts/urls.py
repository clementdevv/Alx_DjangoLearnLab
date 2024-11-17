from django.urls import path
from .views import *

urlpatterns = [  
    #User related URL definition
    path('users/', user_list, name='user-list'),                # List all users
    path('users/<int:pk>/', user_detail, name='user-detail'),   # Retrieve user by ID
    path('users/<int:pk>/update/', update_user, name='user-update'),  # Update user
    path('users/<int:pk>/delete/', delete_user, name='user-delete'),  # Delete user               
               
    #Authentication Process route definition
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('token_test/', test_token,),
    
    #Follow management route definition
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
    path('followers/', list_followers, name='list-followers'),
    path('following/', list_following, name='list-following'),

]
