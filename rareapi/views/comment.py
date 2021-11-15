"""View module for handling requests about games"""
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Comment, RareUser
from django.contrib.auth.models import User
from rareapi.models.post import Post

class CommentView(ViewSet):

    def list(self, request):
        try:
            comments = Comment.objects.all()
            serializer = CommentSerializer(
                comments, many=True, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            post = Post.objects.get(pk=request.data["postId"])
            author = RareUser.objects.get(pk=request.data["userId"])
            comment = Comment.objects.create(
                post=post,
                author=author,
                content=request.data["content"],
                created_on=request.data["createdOn"]
            )
            serializer = CommentSerializer(
                comment, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        try:
            post = Post.objects.get(pk=request.data["postId"])
            author = RareUser.objects.get(pk=request.data["userId"])
            comment = Comment.objects.get(pk=pk)
            comment.post = post
            comment.author = author
            comment.content = request.data["content"]
            comment.created_on = request.data["createdOn"]
            comment.save()
            return Response("Comment updated", status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response("Comment does not exist.", status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response("Comment deleted.", status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response("Comment does not exist.")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)


class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = RareUser
        fields = ('user', 'profile_image_url',)


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_on')
