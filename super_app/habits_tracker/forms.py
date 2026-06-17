from django import forms
from .models import Habit, TrackedHabit

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        exclude = ('user',)


class TrackedHabitForm(forms.ModelForm):
    class Meta:
        model = TrackedHabit
        fields = ('is_done',)