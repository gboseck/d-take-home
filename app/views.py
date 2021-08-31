from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


@api_view(["POST"])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def top_posts(request):
    posts = Post.objects.all()
    if posts:
        post_serializer = PostSerializer(posts, many=True)

        post_count = {}

        for post in post_serializer.data:
            try:
                post_count[post["user"]] += 1
            except KeyError:
                post_count[post["user"]] = 1

        sorted_post_count = (sorted(post_count.items(),
                                    key=lambda x: x[1],
                                    reverse=True))
        output = []

        for post in sorted_post_count:
            user = User.objects.get(pk=post[0])
            user_serializer = UserSerializer(user)
            output.append({"username": user_serializer.data["username"],
                           "posts": post[1]})

        return Response(output, status=status.HTTP_200_OK)
    elif not posts:
        return Response("No posts found!", status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response("No users found!", status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def follow_user(request):
    serializer = FollowUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response("Invalid request body!", status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(pk=request.data["user"])
    following_user = User.objects.get(pk=request.data["following_user"])

    if user and following_user:
        user.profile.followers.add(following_user)
        user.save()
        return Response("Follow successful!", status=status.HTTP_201_CREATED)
    else:
        return Response("One or both user IDs do not exist!", status=status.HTTP_400_BAD_REQUEST)