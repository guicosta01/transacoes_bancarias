from django.db import models

from django.db import models

class Transacao(models.Model):
    IDENTIFICADOR_CHOICES = (
        ('gerado', 'Gerado pela API'),
        ('manual', 'Manual'),
    )
    
    MODO_CHOICES = (
        ('dinheiro', 'Dinheiro'),
        ('cartao_debito', 'Cartão de Débito'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('transferencia', 'Transferência Bancária'),
    )
    
    TIPO_CHOICES = (
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    )

    identificador = models.CharField(max_length=7, choices=IDENTIFICADOR_CHOICES, default='gerado')
    data_hora_transacao = models.DateTimeField()
    modo_transacao = models.CharField(max_length=15, choices=MODO_CHOICES)
    categoria = models.CharField(max_length=255)
    nota_observacao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_transacao = models.CharField(max_length=10, choices=TIPO_CHOICES)

    def save(self, *args, **kwargs):
        if self.identificador == 'gerado':
            # Lógica para gerar o identificador quando a transação for válida
            # Por exemplo: self.identificador = 'T' + str(self.pk)
            pass
        super(Transacao, self).save(*args, **kwargs)

    def __str__(self):
        return f"Transacao {self.id}"

