from django.urls import path
from .views import signupView, registerView, logoutView

app_name = 'accounts'

urlpatterns = [
    path('logout/', logoutView, name='logout'),
    path('register/', registerView, name='register'),
    path('signup/', signupView, name='signup'),
]