from django.db import models
from django.contrib.auth.models import User
from .story import Story


class Comment(models.Model):

    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=False)

    @property
    def is_current_user(self):
        return self.__is_current_user
        
    @is_current_user.setter
    def is_current_user(self, value):
        self.__is_current_user = value