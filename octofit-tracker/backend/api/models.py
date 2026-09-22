from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    motto = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    ACTIVITY_TYPES = (
        ('running', 'Running'),
        ('walking', 'Walking'),
        ('strength', 'Strength training'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration_minutes = models.PositiveIntegerField()
    points = models.PositiveIntegerField(default=0)
    recorded_at = models.DateTimeField()

    class Meta:
        ordering = ('-recorded_at',)

    def __str__(self):
        return f'{self.user.username}: {self.activity_type}'


class LeaderboardEntry(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='leaderboard_entry')
    points = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('rank', 'team__name')

    def __str__(self):
        return f'{self.team.name}: {self.points}'


class Workout(models.Model):
    LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    title = models.CharField(max_length=120)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVELS)
    focus = models.CharField(max_length=80)

    def __str__(self):
        return self.title