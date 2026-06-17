import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from habits_tracker.models import Habit, TrackedHabit, Serie
from django.db.models import OuterRef, Subquery, Value

User = get_user_model()

def check_all_user_habits_for_today():
    today = timezone.now().date()
    check_all_users_habits(today)


def check_all_users_habits(date:datetime.date):
    users = User.objects.filter()
    for user in users:
        check_user_habit(user, date)


def check_user_habit(user: User, yesterday):
    current_tracked_habit = TrackedHabit.objects.filter(
        date=Value(yesterday),
        habit=OuterRef('pk'),)
    habits = Habit.objects.filter(
        user=user).annotate(
        current_tracked_is_done=Subquery(current_tracked_habit.values('is_done')[:1]),)
    user_serie = Serie.objects.get_or_create(user=user,)[0]

    is_user_lose_serie = False
    if len(habits) == 0:
        return

    for habit in habits:
        if habit.current_tracked_is_done is None:
            create_not_completed_yesterday_tracked_habit(habit=habit,
                                                         is_done=False,
                                                         date=yesterday)
            is_user_lose_serie = True
        elif habit.current_tracked_is_done is False:
            is_user_lose_serie = True
        elif habit.current_tracked_is_done is True:
            continue

    change_serie(user_serie, is_user_lose_serie)


def change_serie(serie: Serie, is_user_lose_serie):
    if is_user_lose_serie:
        if serie.current_day_count > serie.best_day_count:
            serie.best_day_count = serie.current_day_count
        serie.current_day_count = 0
    else:
        serie.current_day_count += 1
        if serie.current_day_count > serie.best_day_count:
            serie.best_day_count = serie.current_day_count
    serie.save()


def create_not_completed_yesterday_tracked_habit(habit, is_done, date):
        TrackedHabit.objects.create(habit=habit,
                                    is_done=is_done,
                                    date=date,)