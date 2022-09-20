from django.db import models
from django.contrib.auth.models import User

class EmailCodes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    code = models.CharField(max_length=6)


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='announcements')
    content = models.TextField()

    def __str__(self):
        return self.title


class Recall(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recalls')    
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='recalls')
    date_create = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    accept = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:50]
