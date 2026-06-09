from django.urls import path
from .views import exchange_rate

app_name = 'exchange_rate'

urlpatterns = [
    path('exchange_rate_chart/', exchange_rate,name='exchange_rate_chart'),
]