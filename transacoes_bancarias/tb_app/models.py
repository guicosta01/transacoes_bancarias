from django.db import models

class Transacao(models.Model):
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

    identificador = models.AutoField(primary_key=True)
    data_hora_transacao = models.DateTimeField()
    modo_transacao = models.CharField(max_length=15, choices=MODO_CHOICES)
    categoria = models.CharField(max_length=255)
    nota_observacao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_transacao = models.CharField(max_length=10, choices=TIPO_CHOICES)

    def save(self, *args, **kwargs):
        # Lógica personalizada, se necessário
        super(Transacao, self).save(*args, **kwargs)

    def __str__(self):
        return f"Transacao {self.identificador}"
        
