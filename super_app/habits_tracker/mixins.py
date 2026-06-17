from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .forms import HabitForm
from .models import Habit
from django.shortcuts import reverse, get_object_or_404


class HabitFormMixin(LoginRequiredMixin):
    model = Habit
    form_class = HabitForm
    def get_success_url(self):
        return reverse('habits_tracker:main_page')

    def dispatch(self, request, *args, **kwargs):
        habit = get_object_or_404(Habit, pk=self.kwargs[self.pk_url_kwarg])
        if habit.user != self.request.user:
            raise PermissionDenied('Permission denied')
        return super().dispatch(request, *args, **kwargs)