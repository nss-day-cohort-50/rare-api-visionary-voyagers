"""View module for handling requests about games"""
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Tag

class TagView(ViewSet):

    def list(self, request):
        try:
            tags = Tag.objects.all()
            serializer = TagSerializer(
                tags, many=True, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(
                tag, many=False, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"message": "Tag not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, pk):
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()
            return Response("Tag deleted")
        except Tag.DoesNotExist:
            return Response({"Tag does not exist."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            tag = Tag.objects.create(
                label=request.data["label"]
            )
            return Response({"Tag created"}, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
            tag.label=request.data["label"]
            tag.save()
            return Response({"Tag updated"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Tag.DoesNotExist:
            return Response({"Tag does not exist."}, status=status.HTTP_404_NOT_FOUND)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'label')
