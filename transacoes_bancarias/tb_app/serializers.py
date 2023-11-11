from rest_framework import serializers
from .models import Transacao
from django.contrib.auth.models import User

class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password', 'email']