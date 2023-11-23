from django.urls import path
from . import views
from .views import TransacaoList

urlpatterns = [
    path('', views.getTransacoes),
    path('create', views.addTransacao),
    path('read/<str:pk>', views.getTransacao),
    path('update/<str:pk>', views.updateTransacao),
    path('delete/<str:pk>', views.deleteTransacao),
    path('remover_transacoes/', views.remover_transacoes),
    path('editar_transacao/', views.editarTransacoes),
    path('signup', views.signup),
    path('login', views.login),
    path('test_token', views.test_token),
    path('list/', TransacaoList.as_view(), name='transacao-list'),
]
