from django.http import JsonResponse
from requests import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from .models import CustomUser 
from .serializers import CustomUserSerializer  


from posts.serializers import CustomUserSerializer
from rest_framework import status

from .serializers import * 
from rest_framework import *
from django.shortcuts import get_object_or_404


User = get_user_model

#User Views For User management:
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer

# class UserListView(generics.GenericAPIView):
    
#     queryset = CustomUser.objects.all()  # Queryset: All users
#     serializer_class = CustomUserSerializer  # Serializer for user data
#     permission_classes = [permissions.IsAuthenticated]  # Restrict to authenticated users only

#     def get(self, request, *args, **kwargs):
#         """
#         Handle GET requests to retrieve the list of users.
#         """
#         users = self.get_queryset()
#         serializer = self.get_serializer(users, many=True)
#         return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def user_list(request):
    queryset = CustomUser.objects.all()
    serializer = CustomUserSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    """
    Retrieve a specific user by ID.
    """
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CustomUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    """
    Update a specific user (profile).
    """
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Allow only the owner to update their profile
    if request.user != user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):
    """
    Delete a user (Only owner can delete their account).
    """
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Only allow the owner to delete their profile
    if request.user != user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    user.delete()
    return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

#Authentication related views
@api_view(['POST']) 
@permission_classes([AllowAny])
def register_view(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'], 
            password=serializer.validated_data['password'],             
        )
        if user:
            token, _ = Token.objects.create(user=user)
            return JsonResponse({"token": token.key}, status=200)
        return JsonResponse({"error": "Invalid credentials"}, status=401)
    return JsonResponse(serializer.errors, status=400)


#token testing (tested via Rest Client vs code extension; in the test.rest file)
@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"authentication passed for {}".format(request.user.email)})



#Follow Management Views:
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):    
    target_user = get_object_or_404(CustomUser, id=user_id)
    
    if request.user == target_user:
        return Response(
            {'error': 'You cannot follow yourself'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    request.user.following.add(target_user)
    
    return Response({
        'message': f'You are now following {target_user.username}',
        'following': CustomUserSerializer(request.user.following.all(), many=True).data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):   
    target_user = get_object_or_404(CustomUser, id=user_id)    
    request.user.following.remove(target_user)    
    return Response({
        'message': f'You have unfollowed {target_user.username}',
        'following': CustomUserSerializer(request.user.following.all(), many=True).data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_followers(request):   
    followers = request.user.followers.all()
    return Response({
        'followers': CustomUserSerializer(followers, many=True).data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_following(request):    
    following = request.user.following.all()
    return Response({
        'following': CustomUserSerializer(following, many=True).data
    })