from django.urls import path
from .views import main_page, HabitCreateView, HabitDeleteView, HabitEditView, TrackedHabitCreateView, TrackedHabitUpdateView, download_data

app_name = 'habits_tracker'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('add_habit/', HabitCreateView.as_view(), name='add_habit'),
    path('edit_habit/<pk>', HabitEditView.as_view(), name='edit_habit'),
    path('delete_habit/<pk>', HabitDeleteView.as_view(), name='delete_habit'),
    path('add_habit_tracked/<pk>', TrackedHabitCreateView.as_view(), name='add_habit_tracked'),
    path('edit_habit_tracked/<pk>', TrackedHabitUpdateView.as_view(), name='edit_habit_tracked'),
    path('download', download_data, name='download'),
]