from django.urls import path
from .views import homepage, nowhere

app_name = 'homepage'

urlpatterns=[
    path('', homepage, name='homepage'),
    path('nowhere/', nowhere, name='nowhere'),
]