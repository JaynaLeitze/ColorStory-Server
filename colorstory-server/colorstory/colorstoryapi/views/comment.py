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
from colorstoryapi.models import Comment


class Comments(ViewSet):

    def create(self, request):
        """Handle POST operations for comments
        Returns:
            Response -- JSON serialized comment instance
        """


        story = Story.objects.get(pk=request.data["story_id"])

        comment = Comment()
        comment.story = story
        comment.author= request.auth.user
        comment.content = request.data["content"]
        comment.created_on = datetime.datetime.now()

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    class Meta:
        model = Comment
        fields = ('id', 'story', 'author', 'content', 'created_on')
        depth = 2

