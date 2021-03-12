from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from colorstoryapi.models import Story
import datetime

class Stories(ViewSet):
    """Public Stories"""
    def list(self, request):
        """Handle GET requests to post resource
        Returns:
            Response -- JSON serialized list of posts
        """   
        stories = Story.objects.filter(private=False)

        serializer = StorySerializer(
            stories, many=True, context={'request': request})
        return Response(serializer.data)

class StorySerializer(serializers.ModelSerializer):
    """JSON serializer for stories
    Arguments:
        serializer type
    """
    class Meta:
        model = Story
        fields = ('id', 'user', 'color', 'word_prompt', 'private', 'title', 'created_on', 'content')
      