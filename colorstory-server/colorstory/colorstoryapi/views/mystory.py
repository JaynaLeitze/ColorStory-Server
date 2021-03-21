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
        # user = User.objects.get(user=request.auth.user)
        story = Story()
        story.user = request.auth.user
        story.color = request.data["color"]
        story.word_prompt = request.data["word_prompt"]
        story.private = request.data["private"]
        story.content = request.data["content"]
        story.title = request.data["title"]
        story.created_on = datetime.date.today()


        try:
            story.save()
            serializer = StorySerializer(story, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single post
        Returns:
            Response -- JSON serialized game instance
        """
        try:
            story = Story.objects.get(user=request.auth.user,pk=pk)

            # if story.user_id == User.id:
            #     story.is_current_user = True
            # else:
                # story.is_current_user = False
            serializer = StorySerializer(story, context={'request': request})

            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a story
        
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            story = Story.objects.get(user=request.auth.user,pk=pk)
            story.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Story.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to post resource
        Returns:
            Response -- JSON serialized list of posts
        """
        # user = User.objects.get(user=request.auth.user)
        stories = Story.objects.filter(user=request.auth.user)

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
        fields = ('id', 'user', 'color', 'word_prompt', 'private', 'title', 'created_on', 'content', 'is_current_user')
        depth = 2