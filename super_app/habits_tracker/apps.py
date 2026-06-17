from django.apps import AppConfig
import sys


class HabitsTrackerConfig(AppConfig):
    name = 'habits_tracker'

    def ready(self):
        if 'runserver' in sys.argv:
            from django_q.models import Schedule
            Schedule.objects.all().delete()
            Schedule.objects.get_or_create(
                #func='habits_tracker.tasks.check_all_user_habits_for_today',
                func='habits_tracker.tasks.check_all_user_habits_for_today',
                schedule_type=Schedule.DAILY,
                #cron='25 16 * * *',
                cron='55 23 * * *',
                repeats=1,
                name='daily_habits_tracker', )