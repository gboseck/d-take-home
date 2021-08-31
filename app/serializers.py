from rest_framework import serializers

from .models import User, Post


class FollowUserSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=True)
    following_user = serializers.IntegerField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
