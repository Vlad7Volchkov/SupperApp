import decimal
from .models import Transaction, IncomeCategory, ExpenseCategory, UserWallet

class TransactionManager:
    @staticmethod
    def save_income_transaction(wallet: UserWallet, amount:decimal.Decimal, category:IncomeCategory):
        if amount < 0:
            raise ValueError('Transaction cant have negative amount')

        transaction = Transaction.objects.create(
            user_wallet = wallet,
            amount = amount,
            income = category,)
        return transaction

    @staticmethod
    def save_expense_transaction(wallet: UserWallet, amount: decimal.Decimal, category_name: str):
        if amount < 0:
            raise ValueError('Сумма не может быть отрицательной')

        if wallet.balance - amount < 0:
            raise ValueError('Кошелёк не может иметь отрицательный баланс')

        category = ExpenseCategory.objects.get_or_create(name=category_name)[0]
        transaction = Transaction.objects.create(
            user_wallet=wallet,
            amount=amount,
            expense=category, )
        return transaction