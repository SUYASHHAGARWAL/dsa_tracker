from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    PLATFORM_CHOICES = [
        ('LeetCode', 'LeetCode'),
        ('GFG', 'GeeksforGeeks'),
        ('Codeforces', 'Codeforces'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    link = models.URLField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='LeetCode')
    status = models.CharField(max_length=20, default='Unsolved')

    def __str__(self):
        return self.title
