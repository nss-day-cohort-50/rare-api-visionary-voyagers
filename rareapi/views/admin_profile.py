from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from django.db.models import Q
from rareapi.models import RareUser

class AdminView(ViewSet):
    def partial_update(self, request, pk=None):
        user = User.objects.get(pk=pk)
        if "is_active" in request.data:
            user.is_active = not user.is_active
            user.save()
            return Response({"message": "User Active Status Changed"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['Get'])
def admin_profile(request):
    admin = RareUser.objects.get(user=request.auth.user)
    if admin.user.is_staff:
        users = RareUser.objects.all().filter(~Q(user = admin.user)).order_by('user__first_name')
        serializer = AuthorSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)
    else:
         return Response({"message":"User is not admin"}, status=status.HTTP_400_BAD_REQUEST)





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name','is_staff', 'username', 'is_active')


class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = RareUser
        fields = ('user', 'profile_image_url',)