from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.db.models import Q

from notifications.models import Notification
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer

# Post Views
@api_view(['GET'])
def view_all_posts(request):    
    search_query = request.query_params.get('search', '')
    posts = Post.objects.filter(
        Q(title__icontains=search_query) | 
        Q(content__icontains=search_query)
    )
    
    # Pagination
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    start = (page - 1) * page_size
    end = start + page_size
    
    serializer = PostSerializer(posts[start:end], many=True)
    return Response({
        'posts': serializer.data,
        'total_posts': posts.count(),
        'page': page,
        'page_size': page_size
    })

@api_view(['GET'])
def view_post_details(request, pk):   
    post = get_object_or_404(Post, pk=pk)
    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):   
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_post(request, pk):    
    post = get_object_or_404(Post, pk=pk)
    
    # Check if the current user is the author
    if post.author != request.user:
        return Response(
            {'error': 'You do not have permission to edit this post'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = PostSerializer(post, data=request.data, partial=bool(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):

    post = get_object_or_404(Post, pk=pk)
    
    # Check if the current user is the author
    if post.author != request.user:
        return Response(
            {'error': 'You do not have permission to delete this post'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Comment Views
@api_view(['GET'])
def view_all_comments(request, post_pk):   
    post = get_object_or_404(Post, pk=post_pk)
    comments = post.comments.all()
    
    # Pagination
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    start = (page - 1) * page_size
    end = start + page_size
    
    serializer = CommentSerializer(comments[start:end], many=True)
    return Response({
        'comments': serializer.data,
        'total_comments': comments.count(),
        'page': page,
        'page_size': page_size
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, post_pk):    
    post = get_object_or_404(Post, pk=post_pk)
    serializer = CommentSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(author=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_comment(request, pk):    
    comment = get_object_or_404(Comment, pk=pk)
    
    # Check if the current user is the comment author
    if comment.author != request.user:
        return Response(
            {'error': 'You do not have permission to edit this comment'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = CommentSerializer(comment, data=request.data, partial=bool(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, pk):   
    comment = get_object_or_404(Comment, pk=pk)
    
    # Check if the current user is the comment author
    if comment.author != request.user:
        return Response(
            {'error': 'You do not have permission to delete this comment'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


#My viewsets
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):       
        serializer.save(author=self.request.user)

    def get_queryset(self):      
        queryset = Post.objects.all()
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset

class CommentViewSet(viewsets.ModelViewSet):   
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):        
        serializer.save(author=self.request.user)

    def get_queryset(self):        
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset
    
    
#User Feed view for generating feeds
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):   
    followed_users = request.user.following.all()
    feed_posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
    
    # Paginate results      
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    start = (page - 1) * page_size
    end = start + page_size
    
    # Serialize and return posts
    serializer = PostSerializer(feed_posts[start:end], many=True)
    
    return Response({
        'feed': serializer.data,
        'total_posts': feed_posts.count(),
        'page': page,
        'page_size': page_size
    })
    
#Like and Unlike Views:
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Post, Like
from notifications.models import Notification

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):   
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        return Response({"detail": "Post already liked"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a notification for the post author
    Notification.objects.create(
        recipient=post.author,
        actor=request.user,
        verb="liked your post",
        target=post
    )

    return Response({"detail": "Post liked successfully"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)

    like = Like.objects.filter(user=request.user, post=post).first()
    if not like:
        return Response({"detail": "Post was not liked"}, status=status.HTTP_400_BAD_REQUEST)

    like.delete()
    return Response({"detail": "Post unliked successfully"}, status=status.HTTP_200_OK)

    
# Post.objects.filter(author__in=following_users).order_by", "permissions.IsAuthenticated
# "generics.get_object_or_404(Post, pk=pk)"