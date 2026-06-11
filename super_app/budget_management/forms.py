from .models import Transaction, IncomeCategory, SavingGoals, ExpenseCategory
from django import forms


class SavingsGoalsForm(forms.ModelForm):
    goal = forms.DecimalField(max_digits=12, decimal_places=2, min_value=1, label='Сумма')
    class Meta:
        model = SavingGoals
        fields = ['description', 'goal']


class IncomeForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, label='Сумма')
    income = forms.ModelChoiceField(queryset=IncomeCategory.objects.all(), label='Категория дохода', required=True)
    class Meta:
        model = Transaction
        fields = ['amount', 'income']


class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        wallet = kwargs.pop('user_wallet', None)
        super(ExpenseForm, self).__init__(*args, **kwargs)
        expense = forms.ModelChoiceField(
            queryset=Transaction.objects.filter(user_wallet=wallet).values('expense'),
            label='Категория расхода',
            required=False,
        )

    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0, label='Сумма')
    expense_text = forms.CharField(required=False, label='Новая категория расхода')
    class Meta:
        model = Transaction
        fields = ['amount', 'expense', 'expense_text']
    def clean(self):
        cleaned_data = super().clean()
        expense = cleaned_data.get('expense')
        expense_text = None if str(cleaned_data.get('expense_text')).strip(' ')=='' else cleaned_data.get('expense_text')

        if expense_text is None and expense is None:
            raise forms.ValidationError('Заполните или новую категорию расхода или выберите старую категорию расхода')
        elif (expense_text is not None) and (expense is not None):
            raise forms.ValidationError('Заполните или новую категорию расхода или выберите старую категорию расхода')
        else:
            return cleaned_data