from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Transacao
from .serializers import TransacaoSerializer

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from rest_framework import generics
from .filters import TransacaoFilter
import django_filters


#================================ Token ================================
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))

#================================ Token ================================

#================================ Filters ================================

class TransacaoList(generics.ListAPIView):
    queryset = Transacao.objects.all()
    serializer_class = TransacaoSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TransacaoFilter


#================================ Filters ================================


#get all transacoes
@api_view(['GET'])
def getTransacoes(request):
    transacoes = Transacao.objects.all()
    serializer = TransacaoSerializer(transacoes, many=True)
    return Response(serializer.data)

#get single transacao
@api_view(['GET'])
def getTransacao(request, pk):
    transacao = Transacao.objects.get(id=pk)
    serializer = TransacaoSerializer(transacao, many=False)
    return Response(serializer.data)

#add transacao
@api_view(['POST'])
def addTransacao(request):
    serializer = TransacaoSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

#update transacao
@api_view(['PUT'])
def updateTransacao(request, pk):
    transacao = Transacao.objects.get(id=pk)
    serializer = TransacaoSerializer(instance=transacao, data = request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


#delete transacao
@api_view(['DELETE'])
def deleteTransacao(request, pk):
    transacao = Transacao.objects.get(id=pk)
    transacao.delete()

    return Response('Transacao successfully deleted')


@api_view(['POST'])
def remover_transacoes(request):
    if request.method == 'POST':
        identificadores = request.data.get('identificadores', [])

        transacoes = Transacao.objects.filter(identificador__in=identificadores)

        if transacoes.exists():
            for transacao in transacoes:
                if transacao.tipo_transacao == 'receita':
                    tipo_estorno = 'despesa'
                elif transacao.tipo_transacao == 'despesa':
                    tipo_estorno = 'receita'
                else:
                    tipo_estorno = None

                if tipo_estorno:
                    estorno = Transacao.objects.create(
                        data_hora_transacao=transacao.data_hora_transacao,
                        modo_transacao=transacao.modo_transacao,
                        categoria=transacao.categoria,
                        nota_observacao=f"Estorno da transação {transacao.identificador}",
                        valor=transacao.valor, 
                        tipo_transacao=tipo_estorno
                    )
                    estorno.save()

            #transacoes.delete()

            return Response({'message': 'Transações removidas e registros de estorno criados com sucesso.'}, status=200)
        else:
            return Response({'message': 'Nenhuma transação encontrada para remover.'}, status=404)


# Sua API deverá ter um endpoint onde o usuário poderá fornecer um conjunto de registros contendo seu identificador junto com valores a serem editados:
# A edição de uma transação acontece primeiro fazendo a remoção do mesmo (pela operação de estorno) e então a criação do novo registro (lançamento retificado);
# Deve ser possível identificar quando um registro foi editado, e o registro mais novo deverá armazenar os identificadores dos registros mais antigos;
@api_view(['POST'])
def editarTransacoes(request):
    if request.method == 'POST':
        registros_editar = request.data.get('identificadores', [])

        for registro in registros_editar:
            identificador = registro.get('identificador')
            novo_valor = registro.get('novo_valor')

            # Buscar a transação existente pelo identificador
            try:
                transacao_existente = Transacao.objects.get(identificador=identificador)

                # Criar nova transação com o novo valor
                transacao_editada = Transacao.objects.create(
                    data_hora_transacao=transacao_existente.data_hora_transacao,
                    modo_transacao=transacao_existente.modo_transacao,
                    categoria=transacao_existente.categoria,
                    nota_observacao=f"Retificado da transação {transacao_existente.identificador}",
                    valor=novo_valor,
                    tipo_transacao=transacao_existente.tipo_transacao
                )
                transacao_editada.save()

                # Estorno da transação antiga
                if transacao_existente.tipo_transacao == 'receita':
                    tipo_estorno = 'despesa'
                elif transacao_existente.tipo_transacao == 'despesa':
                    tipo_estorno = 'receita'
                else:
                    tipo_estorno = None

                if tipo_estorno:
                    estorno = Transacao.objects.create(
                        data_hora_transacao=transacao_existente.data_hora_transacao,
                        modo_transacao=transacao_existente.modo_transacao,
                        categoria=transacao_existente.categoria,
                        nota_observacao=f"Estorno da transação {transacao_existente.identificador}",
                        valor=transacao_existente.valor,
                        tipo_transacao=tipo_estorno
                    )
                    estorno.save()

                # Atualizar a transação editada com a referência da transação anterior
                #transacao_editada.transacao_anterior = transacao_existente
                #transacao_editada.save()

                # Remover a transação antiga
                #transacao_existente.delete()

            except Transacao.DoesNotExist:
                return Response({'message': f'Transação com identificador {identificador} não encontrada.'}, status=404)

        return Response({'message': 'Transações editadas com sucesso.'}, status=200)
    else:
        return Response({'message': 'Método não permitido.'}, status=405)

