from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    Team = [
        ('Development', 'Development'),
        ('Product', 'Product'),
        ('Design', 'Design'),
        ('Human', 'Human'),
        ('Resource', 'Resource'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True, unique=True)
    designation = models.CharField(max_length=51, null=True, blank=True, choices=Team)
    profile_picture = models.ImageField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
