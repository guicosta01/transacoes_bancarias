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
