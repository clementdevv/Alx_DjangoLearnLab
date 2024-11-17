from rest_framework import serializers
from django.contrib.auth import get_user_model 
from rest_framework.authtoken.models import Token

from accounts.models import CustomUser

# User = get_user_model()  

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'following'
        ]
        extra_kwargs = {
            'followers': {'read_only': True},  # Followers cannot be edited directly
            'following': {'read_only': True},
        }
        
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email = validated_data.get('email', ''),
            password = validated_data['password'], 
            bio = validated_data.get('bio', ''), 
            profile_picture = validated_data.get('profile_picture', None),
        )
        token, created = Token.objects.create(user=user)
        # Attach the token to the serializer instance
        user.token = token.key
        return user

    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)