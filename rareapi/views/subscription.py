"""View module for handling requests about games"""
from rareapi.models.rare_user import RareUser
from rest_framework import status
from django.contrib.auth import get_user_model
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, Subscription, subscription
from rest_framework.decorators import action
from django.contrib.auth.models import User
from datetime import datetime


class SubscriptionView(ViewSet):
    def list(self, request):

        subscriptions = Subscription.objects.all()

        serializer = SubscriptionSerializer(
            subscriptions, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        user = RareUser.objects.get(user=request.auth.user)
        subscription = Subscription.objects.create(
            follower=user,
            author=RareUser.objects.get(pk=request.data["followerId"]),
            created_on=datetime.now().strftime("%Y-%m-%d"),
            ended_on="9999-01-01"
        )
        serializer = SubscriptionSerializer(
            subscription, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk):
        subscription = Subscription.objects.get(pk=pk)
        subscription.ended_on = datetime.now().strftime("%Y-%m-%d")
        subscription.save()
        return Response({"message": "You have unsubscribed from this user."}, status=status.HTTP_204_NO_CONTENT)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = RareUser
        fields = ('user',)


class SubscriptionSerializer(serializers.ModelSerializer):
    follower = RareUserSerializer()
    author = RareUserSerializer()

    class Meta:
        model = Subscription
        fields = ('id', 'author', 'follower', 'created_on', 'ended_on')
