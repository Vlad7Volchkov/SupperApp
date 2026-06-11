from django.apps import AppConfig
import sys


class BudgetManagementConfig(AppConfig):
    name = 'budget_management'

    def ready(self):
        if 'runserver' in sys.argv:
            from .models import IncomeCategory
            incomes = [
                'Стипендия',
                'Подработка',
                'Работа',
                'Пенсия',
                'Пассивный доход',
                'Предпринимательский доход',
                'Инвестиции',
                'Банковские вклады',
                'Льготы',
                'Фриланс',
                'Самозанятость'
            ]
            for income in incomes:
                IncomeCategory.objects.get_or_create(name=income)