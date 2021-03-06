"""View module for handling requests about games"""
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Comment, RareUser
from django.contrib.auth.models import User
from rareapi.models.post import Post
from datetime import datetime
class CommentView(ViewSet):

    def list(self, request):
        try:
            post_id = self.request.query_params.get('postId', None)
            author = RareUser.objects.get(user=request.auth.user)
            post = Post.objects.get(pk=post_id)
            comments = Comment.objects.all().filter(post=post).order_by('-created_on')
            for comment in comments:
                comment.is_author = comment.author == author
            serializer = CommentSerializer(
                comments, many=True, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            post = Post.objects.get(pk=request.data["postId"])
            author = RareUser.objects.get(user=request.auth.user)
            comment = Comment.objects.create(
                post=post,
                author=author,
                content=request.data["content"],
                created_on= datetime.now().strftime ("%Y-%m-%d") 
            )
            serializer = CommentSerializer(
                comment, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        try:
            post = Post.objects.get(pk=request.data["postId"])
            author = RareUser.objects.get(user=request.auth.user)
            comment = Comment.objects.get(pk=pk)
            comment.post = post
            comment.author = author
            comment.content = request.data["content"]
            comment.created_on = datetime.now().strftime ("%Y-%m-%d") 
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
    is_author = serializers.BooleanField(required=False)
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_on','is_author')
