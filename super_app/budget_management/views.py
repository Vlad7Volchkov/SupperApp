from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserWallet, Transaction, SavingGoals
from .forms import IncomeForm, ExpenseForm, SavingsGoalsForm
from.transactionManager import TransactionManager
from .plotly_func import make_pie_chart
from django import http
from django.views.generic import DetailView


class SavingGoalsView(DetailView):
    model = SavingGoals

@login_required(login_url='/accounts/register/')
def wallet_view(request):
    wallet = UserWallet.objects.get_or_create(user=request.user)[0]
    transactions = Transaction.objects.filter(user_wallet=wallet.pk).order_by('-created_at')[:10]
    saving_goals = SavingGoals.objects.filter(user_wallet=wallet.pk)
    pie = make_pie_chart(wallet)

    context = {'wallet': wallet, 'transactions': transactions, 'saving_goals': saving_goals, 'pie': pie}
    form_savings = SavingsGoalsForm()

    if request.method == 'POST':
        form_savings = SavingsGoalsForm(request.POST)
        if form_savings.is_valid():
            goal = form_savings.cleaned_data['goal']
            description = form_savings.cleaned_data['description']
            saving_goal = SavingGoals.objects.create(user_wallet=wallet, goal=goal, description=description)
            saving_goal.save()
            return http.HttpResponseRedirect('')

    context['form_savings'] = form_savings
    return render(request, 'budget_management/wallet.html', context)

@login_required(login_url='/accounts/register/')
def add_income_view(request):
    wallet = UserWallet.objects.get_or_create(user=request.user)[0]

    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            income = form.cleaned_data['income']
            TransactionManager.save_income_transaction(wallet, amount, income)
            return http.HttpResponseRedirect('')
    else:
        form = IncomeForm()
    context = {'form': form}
    return render(request, 'budget_management/add_income.html', context)

@login_required(login_url='/accounts/register/')
def add_expense_view(request):
    wallet = UserWallet.objects.get_or_create(user=request.user)[0]

    if request.method == 'POST':
        form = ExpenseForm(request.POST, user_wallet=wallet)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            expense = form.cleaned_data['expense']
            expense_text = form.cleaned_data['expense_text']
            try:
                if expense is None:
                    TransactionManager.save_expense_transaction(wallet, amount, expense_text)
                else:
                    TransactionManager.save_expense_transaction(wallet, amount, expense.name)
                return http.HttpResponseRedirect('')
            except ValueError as e:
                form.errors['expense'] = str(e)
    else:
        form = ExpenseForm(user_wallet=wallet)
    context = {'form': form}
    return render(request, 'budget_management/add_expense.html', context)