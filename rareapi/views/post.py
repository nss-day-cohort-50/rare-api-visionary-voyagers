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
from rareapi.models import Post, Category
from rest_framework.decorators import action
from django.contrib.auth.models import User
from datetime import datetime


class PostView(ViewSet):
    def list(self, request):

        posts = Post.objects.all()
        user = RareUser.objects.get(user=request.auth.user)

        user_post = self.request.query_params.get('postsbyuser', None)
        if user_post is not None:
            posts = Post.objects.filter(user=user)

        for post in posts:
            post.is_author = post.user == user
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
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

    def update(self, request, pk):
        user = RareUser.objects.get(user=request.auth.user)

        try:
            post = Post.objects.get(pk=pk)

            post.category = Category.objects.get(pk=request.data['categoryId'])
            post.title = request.data['title']
            post.publication_date = request.data['date']
            post.image_url = request.data['imageUrl']
            post.content = request.data['content']
            post.approved = request.data['approved']
            post.user = user
            post.save()
            return Response({"message": "Updated Post"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist as ex:
            return Response({"Message": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        user = RareUser.objects.get(user=request.auth.user)
        try:
            post = Post.objects.create(
                user=user,
                category=Category.objects.get(pk=request.data['categoryId']),
                title=request.data['title'],
                publication_date=datetime.now().strftime("%Y-%m-%d"),
                image_url=request.data['imageUrl'],
                content=request.data['content'],
                approved=request.data['approved']
            )
            serializer = PostSerializer(
                post, many=False, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        fields = ('id', 'user', 'category', 'title', 'publication_date',
                  'image_url', 'content', 'approved', 'is_author')
        depth = 1
