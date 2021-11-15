"""View module for handling requests about games"""
from rareapi.models.rare_user import RareUser
from django.core.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post
from rest_framework.decorators import action
from django.contrib.auth.models import User

class PostView(ViewSet):
    def list(self, request):

        posts = Post.objects.all()
        user = RareUser.objects.get(user=request.auth.user)

        user_post = self.request.query_params.get('postbyuser', None)
        if user_post is not None:
            posts = Post.objects.filter(user = user_post)

        for post in posts:
            post.is_author = post.user == user
        serializer = PostSerializer(posts, many=True, context = {'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        user = RareUser.objects.get(user=request.auth.user)
        try:
            post = Post.objects.get(pk=pk)
            post.is_author = post.user == user
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

class PostUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = RareUser
        fields = ('user', 'profile_image_url',)

class PostSerializer(serializers.ModelSerializer):
    user = PostUserSerializer()
    is_author = serializers.BooleanField(required=False)
    class Meta:
        model = Post
        fields = ('id', 'user', 'category', 'title', 'publication_date', 'image_url', 'content', 'approved', 'is_author')
        depth = 1