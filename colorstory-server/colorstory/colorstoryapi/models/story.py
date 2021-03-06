from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=10)
    word_prompt = models.CharField(max_length=30)
    private = models.BooleanField()
    content = models.TextField(max_length=2000)
    title = models.CharField(max_length=30)
    created_on = models.DateField(auto_now=False, auto_now_add=False)

    @property
    def is_current_user(self):
        return self.__is_current_user
