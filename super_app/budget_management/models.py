from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class UserWallet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name = 'Пользователь')
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2,
    )

    @property
    def __balance(self):
        balance = 0
        incomes = Transaction.objects.filter(user_wallet=self.user.id, income__isnull=False)
        expenses = Transaction.objects.filter(user_wallet=self.user.id, expense__isnull=False)
        for income in incomes:
            balance += income.amount
        for expense in expenses:
            balance -= expense.amount
        return balance

    def save(self, *args, **kwargs):
        self.balance = self.__balance
        super().save(*args, **kwargs)


class IncomeCategory(models.Model):
    name = models.CharField(verbose_name='Описание', max_length=50)
    def __str__(self):
        return self.name


class ExpenseCategory(models.Model):
    name = models.CharField(verbose_name='Описание', max_length=50)
    def __str__(self):
        return self.name

class Transaction(models.Model):
    user_wallet = models.ForeignKey(
        UserWallet,
        verbose_name='Кошелек',
        on_delete=models.CASCADE,
        related_name='transactions',)
    amount = models.DecimalField(
        'Сумма',
        default=0,
        max_digits=12,
        decimal_places=2,)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    income = models.ForeignKey(
        IncomeCategory,
        verbose_name='Категория дохода',
        on_delete=models.CASCADE,
        null=True,
        blank=True,)
    expense = models.ForeignKey(
        ExpenseCategory,
        verbose_name='Категория расхода',
        on_delete=models.CASCADE,
        null=True,
        blank=True,)

    def save(self, *args, **kwargs):
        if (self.expense is not None) and (self.income is not None):
            raise ValueError('Transaction can\'t have both expense and income')

        super().save(*args, **kwargs)

        self.user_wallet.save()


class SavingGoals(models.Model):

    user_wallet = models.ForeignKey(
        UserWallet,
        verbose_name='Цели накоплений',
        on_delete=models.CASCADE,
        related_name='saving_goals',)

    goal = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2,)

    description = models.CharField(verbose_name='Описание', max_length=50)

    @property
    def is_completed(self):
        if self.goal > self.user_wallet.balance:
            return False
        return True

    @property
    def remained_part(self):
        balance = self.user_wallet.balance
        if balance < self.goal:
            return self.goal - balance
        else:
            return self.goal