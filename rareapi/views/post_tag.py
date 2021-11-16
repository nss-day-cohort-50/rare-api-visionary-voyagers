"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import PostTag


class PostTagView(ViewSet):
    """Level up game types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            post_tag = PostTag.objects.get(pk=pk)
            serializer = PostTagSerializer(post_tag, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all game types
        Returns:
            Response -- JSON serialized list of game types
        """
        post_tags = PostTag.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PostTagSerializer(
            post_tags, many=True, context={'request': request})
        return Response(serializer.data)

class PostTagSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    Arguments:
        serializers
    """
    class Meta:
        model = PostTag
        fields = ('id', 'tag', 'post' )
        depth = 1