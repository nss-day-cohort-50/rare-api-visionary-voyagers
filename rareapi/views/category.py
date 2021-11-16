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
from rareapi.models import  Category
from rest_framework.decorators import action


class CategoryView(ViewSet):
    def list(self,request):
        categories = Category.objects.all().order_by('label')
        serializer = CategorySerializer(categories, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, many=False, context={"request": request})
            return Response(serializer.data)
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist as ex:
            return Response({"Message", "Item does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"Message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def create(self, request):
        try:
            Category.objects.create(
                label = request.data['label']
            )
            return Response({"Message": "Category Created"}, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"Message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def update(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.label = request.data["label"]
            category.save()
            return Response({"Message":"Updated Category"}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist as ex:
            return Response({"Message": ex.ars[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"Message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", "label")