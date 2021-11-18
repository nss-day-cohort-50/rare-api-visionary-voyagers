from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from django.db.models import Q
from rareapi.models import RareUser, Post, Tag, PostTag

@api_view(['Get'])
def user_profile(request):
    user_id = request.query_params.get('userId', None)
    if user_id is not None:
        user = RareUser.objects.get(pk=user_id)
        post = user.post_set.all()
        user = AuthorSerializer(user, context={'reuqest':request})
        post = PostSerializer(post, many=True, context={"request": request})
        profile = {
            "user": user.data,
            "post": post.data
        }
        return Response(profile)
    else:
        return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['Get'])
def users_list(request):
    try:
        users = RareUser.objects.all().order_by("user__first_name")
        serializer = AuthorSerializer(users, many=True, context={"request", request})
        return Response(serializer.data)
    except Exception as ex:
        return Response({"message": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name','is_staff', 'username', 'is_active','date_joined', 'is_staff','email')


class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = RareUser
        fields = ('id','user', 'profile_image_url','active')

class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ('id', 'post', 'tag')
        depth = 1




class PostSerializer(serializers.ModelSerializer):
    is_author = serializers.BooleanField(required=False)

    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date',
                  'image_url', 'content', 'approved', 'is_author', 'tags')
        depth = 1
