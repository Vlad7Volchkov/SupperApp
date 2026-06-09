from locale import currency

from django.shortcuts import render
from .cbr_api import CBRClient
from .plotly_func import  make_exchange_rate_graph
from .forms import ExchangeRateDateForm, CurrencyForm
from .models import Currency


def exchange_rate(request):
    if Currency.objects.count() == 0:
        client = CBRClient('https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL')
        client.set_data_to_db_for_currencies()

    form_date = ExchangeRateDateForm(request.GET)
    form_currency = CurrencyForm(request.GET)
    context = {'form_date': form_date,
               'form_currency': form_currency,}
    if request.method == 'GET':
        if form_date.is_valid():
            date_from = form_date.cleaned_data['date_from']
            date_to = form_date.cleaned_data['date_to']
        else:
            date_from = None
            date_to = None

        if form_currency.is_valid():
            currency_ids = form_currency['currencies'].value()
        else:
            currency_ids = None

        try:
            if date_from is None or date_to is None:
                raise Exception('Invalid form data')
            client = CBRClient('https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL')
            print(f'{date_from} \n {date_to}')
            data = client.get_exchange_rate_for_several_currency(date_from, date_to, currency_ids)
            graph = make_exchange_rate_graph(data)
            context['graph'] = graph
        except Exception:
            context['graph'] = 'При получении данных произошла ошибка'
    return render(request, 'exchange_rate/exchange_rate_chart.html', context)