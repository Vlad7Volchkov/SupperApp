from django import forms
from exchange_rate.models import Currency
import datetime


class ExchangeRateDateForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label='Дата от')
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label='Дата до')

    def clean_date_from(self):
        date_from = self.cleaned_data['date_from']
        if date_from is None:
            return day_two_weeks_ago()
        return date_from

    def clean_date_to(self):
        date_to = self.cleaned_data['date_to']
        if date_to is None:
            return datetime.date.today()
        return date_to

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data['date_from']
        date_to = cleaned_data['date_to']
        if date_from > date_to:
            raise forms.ValidationError('Начало временного периода не может быть больше конца')
        return cleaned_data

class CurrencyForm(forms.Form):
    currencies = forms.ModelMultipleChoiceField(
                            queryset=Currency.objects.all(),
                            widget=forms.SelectMultiple,
                            label='Валюты',
                            required=False,)


def day_two_weeks_ago():
    today = datetime.date.today()
    return today - datetime.timedelta(days=14)