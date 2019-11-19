from django.db import models
from django.contrib.auth.models import User

class Endereco(models.Model):
    rua = models.CharField(max_length=200)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=200)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Endereços"

    def __str__(self):
        return self.rua

class Produto(models.Model):

    nome = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, help_text="EX.:arroz-tio")
    valor = models.DecimalField(decimal_places=2,max_digits=8)
    obsevacoes = models.TextField()
    data_validade = models.DateTimeField()
    peso = models.DecimalField(decimal_places=2,max_digits=5)

    class Meta:
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    comprador = models.ForeignKey("Pessoa", on_delete=models.PROTECT)
    produtos = models.ManyToManyField(Produto)

    
    class Meta:
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return self.pk

class Pessoa(models.Model):

    GENERO_CHOICES = (
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("O", "Outro"),
    )

    nome = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, help_text="EX.:nome-sobrenome")
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    cpf = models.CharField(max_length=11, help_text="EX.: 99999999999")
    telefone_celular = models.CharField(max_length=14, help_text="EX.:99999999999999")
    telefone_fixo = models.CharField(max_length=13, null=True, blank=True, help_text="EX.:9999999999999")
    idade = models.IntegerField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT)
    


class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    telefone_celular = models.CharField(max_length=14, help_text="EX.:99999999999999")
    telefone_fixo = models.CharField(max_length=13, null=True, blank=True, help_text="EX.:9999999999999")
    cnpj = models.CharField(max_length=18, help_text="99.999.999/9999-99")
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT)
    

    class Meta:
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nome