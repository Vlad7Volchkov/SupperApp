from django.urls import path
from .views import wallet_view, add_income_view, add_expense_view

app_name = 'budget_management'

urlpatterns = [
    path('wallet/', wallet_view, name='wallet'),
    path('wallet/add_income/', add_income_view, name='add_income'),
    path('wallet/add_expense/', add_expense_view, name='add_expense'),
]