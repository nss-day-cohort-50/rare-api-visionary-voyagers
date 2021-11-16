"""View module for handling requests about games"""
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Reaction

class ReactionView(ViewSet):

    def list(self, request):
        try:
            reactions = Reaction.objects.all()
            serializer = ReactionSerializer(
                reactions, many=True, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk):
        try:
            reaction = Reaction.objects.get(pk=pk)
            serializer = ReactionSerializer(
                reaction, many=False, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"message": "Reaction not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self,request, pk):
        try:
            reaction = Reaction.objects.get(pk=pk)
            reaction.delete()
            return Response("Reaction deleted")
        except Reaction.DoesNotExist:
            return Response({"Reaction does not exist."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            reaction = Reaction.objects.create(
                label=request.data["label"],
                image_url = request.data["imageUrl"]
            )
            return Response({"Reaction created"}, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, pk):
        try:
            reaction = Reaction.objects.get(pk=pk)
            reaction.label=request.data["label"]
            reaction.save()
            return Response({"Reaction updated"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Reaction.DoesNotExist:
            return Response({"Reaction does not exist."}, status=status.HTTP_404_NOT_FOUND)


class ReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')
