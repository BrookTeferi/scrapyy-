from django.db import models
from django.contrib.auth.models import User

class Auction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = deadline = models.DateTimeField(null=True, blank=True)
    url = models.URLField()
    source = models.CharField(max_length=100)
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserPreference(models.Model):
    keyword = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.keyword}"