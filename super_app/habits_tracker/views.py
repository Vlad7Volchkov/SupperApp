from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import OuterRef, Subquery, Value
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.utils import timezone
from .forms import HabitForm, TrackedHabitForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from .mixins import HabitFormMixin
from .models import Habit, TrackedHabit, Serie

current_date = timezone.now().date()

@login_required(login_url='/accounts/register/')
def main_page(request):
    user = request.user
    current_tracked_habit = TrackedHabit.objects.filter(
        date=Value(current_date),
        habit=OuterRef('pk'),)
    habits = Habit.objects.filter(
        user=user.id).annotate(
        current_tracked_id=Subquery(current_tracked_habit.values('pk')[:1]),
    )
    serie = Serie.objects.get_or_create(user=user.id,)[0]
    context = {'habits': habits, 'serie': serie}
    return render(request, 'habits_tracker/main_page.html', context)


class TrackedHabitCreateView(LoginRequiredMixin, CreateView):
    model = TrackedHabit
    form_class = TrackedHabitForm
    template_name = 'habits_tracker/add_habit_tracked.html'

    def get_success_url(self):
        return reverse('habits_tracker:main_page')

    def form_valid(self, form):
        habit = self.kwargs.get('habit')
        form.instance.habit = habit

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        habit = get_object_or_404(Habit, pk=pk)
        if habit.user != self.request.user:
            raise PermissionDenied('Permission denied')
        self.kwargs['habit'] = habit

        try:
            tracked_habit = TrackedHabit.objects.get(
                date=Value(current_date),
                habit=habit)
            return redirect(reverse('habits_tracker:edit_habit_tracked', kwargs={'pk': tracked_habit.id}))
        except TrackedHabit.DoesNotExist:
            return super().dispatch(request, *args, **kwargs)


class TrackedHabitUpdateView(LoginRequiredMixin, UpdateView):
    model = TrackedHabit
    form_class = TrackedHabitForm
    template_name = 'habits_tracker/add_habit_tracked.html'

    def get_success_url(self):
        return reverse('habits_tracker:main_page')

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        tracked_habit = get_object_or_404(TrackedHabit, pk=pk)

        if tracked_habit.habit.user != self.request.user:
            raise PermissionDenied('Permission denied')

        return super().dispatch(request, *args, **kwargs)


class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm
    template_name = 'habits_tracker/add_habit.html'

    def get_success_url(self):
        return reverse('habits_tracker:main_page')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class HabitEditView(HabitFormMixin, UpdateView):
    template_name = 'habits_tracker/edit_habit.html'


class HabitDeleteView(HabitFormMixin, DeleteView):
    template_name = 'habits_tracker/delete_habit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = HabitForm(instance=self.object)
        return context


@login_required(login_url='/accounts/register/')
def download_data(request):
    data = dict()
    data['habits']={}
    habits = Habit.objects.filter(user=request.user,)
    serie = Serie.objects.filter(user=request.user)[0]
    for habit in habits:
            data['habits'][habit.id] = {}
            data['habits'][habit.id]['name'] = habit.name
            data['habits'][habit.id]['description'] = habit.description
            data['habits'][habit.id]['tracked'] = {}
            tracked_habits = TrackedHabit.objects.filter(habit=habit.id)
            for tracked_habit in tracked_habits:
                data['habits'][habit.id]['tracked'][tracked_habit.id] = {}
                data['habits'][habit.id]['tracked'][tracked_habit.id]['is_done'] = tracked_habit.is_done
                data['habits'][habit.id]['tracked'][tracked_habit.id]['date'] = tracked_habit.date
    data['serie'] = {}
    data['serie']['current_day_count'] = serie.current_day_count
    data['serie']['best_day_count'] = serie.best_day_count
    return JsonResponse(data, safe=False)