from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profileimg = models.ImageField(upload_to='profile_images')

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    title = models.TextField(max_length=20)
    body = models.TextField()
    post_d = models.TextField(default=datetime.now)
    post_t = models.TextField(default=datetime.now)
    created_at = models.DateTimeField(default=datetime.now)

    def __self__(self):
        return self.user
