# filters.py
import django_filters
from .models import Transacao

class TransacaoFilter(django_filters.FilterSet):
    ano = django_filters.NumberFilter(field_name='data_hora_transacao__year')
    mes = django_filters.NumberFilter(field_name='data_hora_transacao__month')
    dia = django_filters.NumberFilter(field_name='data_hora_transacao__day')

    class Meta:
        model = Transacao
        fields = ['ano', 'mes', 'dia']
