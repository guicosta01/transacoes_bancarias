# filters.py
import django_filters
from .models import Transacao

class TransacaoFilter(django_filters.FilterSet):
    ano = django_filters.NumberFilter(field_name='data_hora_transacao__year')
    mes = django_filters.NumberFilter(field_name='data_hora_transacao__month')
    dia = django_filters.NumberFilter(field_name='data_hora_transacao__day')
    categoria = django_filters.CharFilter(lookup_expr='iexact')
    tipo_transacao = django_filters.CharFilter(lookup_expr='iexact')
    modo_transacao = django_filters.CharFilter(lookup_expr='iexact')

    valor_maior_que = django_filters.NumberFilter(field_name='valor', lookup_expr='gt')
    valor_menor_que = django_filters.NumberFilter(field_name='valor', lookup_expr='lt')


    removido = django_filters.BooleanFilter(field_name='nota_observacao', method='get_removido')
    editado = django_filters.BooleanFilter(field_name='nota_observacao', method='get_editado')


    class Meta:
        model = Transacao
        fields = ['ano', 'mes', 'dia','categoria','tipo_transacao','modo_transacao','valor_maior_que','valor_menor_que','removido','editado']

    def get_removido(self, queryset, name, value):
        if value:
            # Filtra transações removidas com base na nota_observacao contendo "Estorno"
            queryset = queryset.filter(nota_observacao__icontains='Estorno')
        else:
            # Se o valor for False, retornar um queryset vazio
            queryset = queryset.none()
        return queryset

    def get_editado(self, queryset, name, value):
        if value:
            # Filtra transações removidas com base na nota_observacao contendo "Estorno"
            queryset = queryset.filter(nota_observacao__icontains='Retificado')
        else:
            # Se o valor for False, retornar um queryset vazio
            queryset = queryset.none()
        return queryset        