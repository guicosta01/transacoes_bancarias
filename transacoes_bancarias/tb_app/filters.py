# filters.py
import django_filters
from .models import Transacao

class TransacaoFilter(django_filters.FilterSet):
    ano = django_filters.NumberFilter(field_name='data_hora_transacao__year')

    class Meta:
        model = Transacao
        fields = ['ano']
