from django.db import models

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

    title = models.CharField(max_length=255)
    link = models.URLField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='LeetCode')
    status = models.CharField(max_length=20, default='Unsolved')

    def __str__(self):
        return self.title
