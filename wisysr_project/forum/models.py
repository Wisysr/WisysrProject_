from django.db import models
import os
import uuid
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.author}'

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"  # Уникальное имя
    return os.path.join(settings.IMAGE_UPLOAD_PATH, new_filename)

class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.ImageField(upload_to=upload_to)  # Поле для хранения изображений
    upload_date = models.DateTimeField(default=now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.file_path.name}"

