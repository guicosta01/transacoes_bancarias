from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Transacao
from .serializers import TransacaoSerializer


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
                        valor=-transacao.valor,  # Valor negativo para estorno
                        tipo_transacao=tipo_estorno
                    )
                    estorno.save()

            transacoes.delete()

            return Response({'message': 'Transações removidas e registros de estorno criados com sucesso.'}, status=200)
        else:
            return Response({'message': 'Nenhuma transação encontrada para remover.'}, status=404)
