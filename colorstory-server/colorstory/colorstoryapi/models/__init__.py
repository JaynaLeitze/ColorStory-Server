from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    color = models.CharField()
    word_prompt = models.CharField()
    private = models.BooleanField()
    content = models.TextField(max_length=2000)
    title = models.CharField(max_length=30)
    created_on = models.DateField(auto_now=False, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
