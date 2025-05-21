from django.db import models

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    STATUS_CHOICES = [
        ('Unsolved', 'Unsolved'),
        ('Solved', 'Solved'),
    ]

    title = models.CharField(max_length=200)
    link = models.URLField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unsolved')

    def __str__(self):
        return self.title
