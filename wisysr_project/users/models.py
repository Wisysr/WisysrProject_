from django.contrib.auth.models import User
from django.db import models
from forum.models import Topic

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
