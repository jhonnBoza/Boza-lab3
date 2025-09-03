from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.CharField(max_length=200, default='👤')
    total_score = models.IntegerField(default=0)
    exams_taken = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"    


  