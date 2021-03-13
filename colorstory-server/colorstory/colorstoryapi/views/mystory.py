from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
import datetime
from colorstoryapi.models import Story


class MyStories(ViewSet):
    """MyStories"""

    def create(self, request):
        """Handle POST operations for events
        Returns:
            Response -- JSON serialized event instance
        """
        user = User.objects.get(user=request.auth.user)
        story = Story()
        story.user = user
        story.title = request.data["title"]
        story.created_on = datetime.datetime.now()
        story.content = request.data["content"]
        story.color = request.data["color"]
        story.word_prompt = request.data["word_prompt"]
        story.private = request.data["private"]


        try:
            story.save()
            serializer = StorySerializer(story, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class StorySerializer(serializers.ModelSerializer):
    """JSON serializer for stories
    Arguments:
        serializer type
    """
    class Meta:
        model = Story
        fields = ('id', 'user', 'color', 'word_prompt', 'private', 'title', 'created_on', 'content')