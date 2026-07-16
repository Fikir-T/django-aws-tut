from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class UserActivity(models.Model):
    """
    This table keep tracks of a user's activity on the website by saving a request from the user on the table.
    It doesn't keep track of every instance of the users status,rather updates the table every time the user sends a request keeping track of the time the user was last online on the website.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} last seen at {self.last_seen}"