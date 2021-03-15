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
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single comment
        Returns:
            Response -- JSON serialized comment instance
        """
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a comment
        Returns:
            Response -- Empty body with 204 status code
        """

        story = Story.objects.get(pk=request.data["story_id"])

        comment = Comment.objects.get(pk=pk)
        comment.story= story
        comment.author= request.auth.user
        comment.content = request.data["content"]
        comment.created_on = datetime.datetime.now()

        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single comment
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to comment resource
        Returns:
            Response -- JSON serialized list of comments
        """
        # Get all commentsfrom the database
        comments = Comment.objects.all()

        # Support filtering comments by type
        #    http://localhost:8000/comments?post_id=1
        #
        # That URL will retrieve all a post's comments
        post = self.request.query_params.get('post_id', None)
        if post is not None:
            comments = comments.filter(post__id=post)

        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    class Meta:
        model = Comment
        fields = ('id', 'story', 'author', 'content', 'created_on')
        depth = 2

