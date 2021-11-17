"""rare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from rareapi.models import Category, Comment, DemotionQueue, PostReaction, PostTag, Post, RareUser, Reaction, Subscription, Tag
from rareapi.views import login_user, register_user, PostView, CategoryView, PostTagView
from rareapi.views.comment import CommentView
from rareapi.views.subscription import SubscriptionView
from rareapi.views.tag import TagView
from rareapi.views.reaction import ReactionView


router=routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostView, 'post')
router.register(r'categories', CategoryView, 'category' )
router.register(r'tags', TagView, 'tag' )
router.register(r'comments', CommentView, 'comment' )
router.register(r'reactions', ReactionView, 'reaction' )
router.register(r'posttags', PostTagView, 'posttag' )
router.register(r'subscriptions', SubscriptionView, 'subscription' )


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('login', login_user)
]
