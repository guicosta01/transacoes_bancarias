from django.urls import path
from . import views

urlpatterns = [
    path('', views.getTransacoes),
    path('create', views.addTransacao),
    path('read/<str:pk>', views.getTransacao),
    path('update/<str:pk>', views.updateTransacao),
    path('delete/<str:pk>', views.deleteTransacao),
]
