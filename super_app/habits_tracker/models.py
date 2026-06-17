from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

class Habit(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='habit',)


class Serie(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='serie',)
    current_day_count = models.IntegerField(default=0)
    best_day_count = models.IntegerField(default=0)

class TrackedHabit(models.Model):
    habit = models.ForeignKey(Habit,
                              on_delete=models.CASCADE,
                              related_name='tracked_habit', )
    is_done = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)