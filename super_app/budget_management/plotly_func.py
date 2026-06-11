import plotly.express as px
from datetime import datetime
from plotly.io import to_html
from .models import Transaction


def make_pie_chart(user_wallet):
    year, month = datetime.now().year, datetime.now().month
    print(year, month)
    expenses_for_month = Transaction.objects.filter(
        user_wallet=user_wallet.id,
        expense__isnull=False,
        created_at__date__year=year,
        created_at__date__month=month,)
    data_x = []
    data_y = []
    for expense in expenses_for_month:
        data_x.append(expense.amount)
        data_y.append(expense.expense.name)

    fig = px.pie(values=data_x, names=data_y)
    return to_html(fig, full_html=False, include_plotlyjs='cnd')
