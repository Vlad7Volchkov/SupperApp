from zeep import Client, helpers
from .models import Currency

class CBRClient:
    def __init__(self, wsdl_url):
        self.client = Client(wsdl_url)

    def set_data_to_db_for_currencies(self):
        Currency.objects.all().delete()
        res = self.client.service.EnumValutes(False)

        valutes = res._value_1._value_1
        for valute in valutes:
            currency_name = str.strip(valute['EnumValutes'].Vname)
            currency_id = str.strip(valute['EnumValutes'].Vcode)
            currency = Currency(name=currency_name, id=currency_id)
            currency.save()

    def get_exchange_rate(self, date_from, date_to, currency_id):
        return self.client.service.GetCursDynamic(date_from, date_to, currency_id)

    def get_exchange_rate_for_several_currency(self, date_from, date_to, currency_ids: list):
        result = {}
        if currency_ids is None:
            return result
        for currency_id in currency_ids:
            currency = Currency.objects.get(id=currency_id)
            exchange_rate = self.get_exchange_rate(date_from, date_to, currency_id)._value_1
            if not hasattr(exchange_rate, '_value_1'):
                continue
            exchange_rate = exchange_rate._value_1
            exchange_rate_data = []
            for i in range(len(exchange_rate)):
                serialized_exchange_rate = helpers.serialize_object(exchange_rate[i]["ValuteCursDynamic"])
                exchange_rate_data.append(serialized_exchange_rate)
            result[currency.name] = exchange_rate_data
        return result