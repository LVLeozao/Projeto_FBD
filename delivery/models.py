from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Endereco(models.Model):
    ESTADO_CHOICE = (
        ('11', 'Rondônia'),
        ('12', 'Acre'),
        ('13', 'Amazonas'),
        ('14', 'Roraima'),
        ('15', 'Pará'),
        ('16', 'Amapá'),
        ('17', 'Tocantins'),
        ('21', 'Maranhão'),
        ('22', 'Piauí'),
        ('23', 'Ceará'),
        ('24', 'Rio Grande do Norte'),
        ('25', 'Paraíba'),
        ('26', 'Pernambuco'),
        ('27', 'Alagoas'),
        ('28', 'Sergipe'),
        ('29', 'Bahia'),
        ('31', 'Minas Gerais'),
        ('32', 'Espírito Santo'),
        ('33', 'Rio de Janeiro'),
        ('35', 'São Paulo'),
        ('41', 'Paraná'),
        ('42', 'Santa Catarina'),
        ('43', 'Rio Grande do Sul'),
        ('50', 'Mato Grosso do Sul'),
        ('51', 'Mato Grosso'),
        ('52', 'Goiás'),
        ('53', 'Distrito Federal'),
    )



    rua = models.CharField(max_length=200)
    numero = models.IntegerField(verbose_name = "Número")
    complemento = models.CharField(max_length=200)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100, choices = ESTADO_CHOICE)
    pais = models.CharField(max_length=2, help_text="EX.: BR", verbose_name = "País")

    class Meta:
        verbose_name_plural = "Endereços"

    def __str__(self):
        return self.rua






class Cliente(models.Model):

    GENERO_CHOICES = (
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("O", "Outro"),
    )

    nome = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, help_text="EX.:nome-segundo", null = True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    cpf = models.CharField(max_length=11, help_text="EX.: 99999999999")
    idade = models.IntegerField()
    endereco = models.ManyToManyField(Endereco)
    telefone1 = models.CharField(max_length=14, help_text="EX.:(99)99999-9999")
    telefone2 = models.CharField(max_length=13, null=True, blank=True, help_text="EX.:(87)3333-3333")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name="getCliente")
    img = models.ImageField(help_text="Tamanho máximo 50x50", verbose_name="Imagem", null = True, blank=True)


    class Meta:
        verbose_name_plural = "Clientes"
        verbose_name = "Cliente"

    def __str__(self):
        return self.nome



class Delivery(models.Model):
    nome_restaurante = models.CharField(max_length=100, help_text="Nome do Delivery: ")
    slug = models.SlugField(max_length=250, help_text="EX.:nome-segundo")
    cnpj = models.CharField(max_length=18, help_text="99.999.999/9999-99", verbose_name="CNPJ")
    endereco = models.ManyToManyField(Endereco)
    descricao = models.TextField(verbose_name="Descrição")
    telefone1 = models.CharField(max_length=14, help_text="EX.:(99)99999-9999")
    telefone2 = models.CharField(max_length=13, null=True, blank=True, help_text="EX.:(87)3333-3333")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name="getDelivery")
    img = models.ImageField(help_text="Tamanho máximo 50x50", verbose_name="Imagem", null = True, blank=True)

    class Meta:
        verbose_name_plural = "Delivery's"
        verbose_name = "Delivery"

    def __str__(self):
        return self.nome_restaurante

    def get_absolute_url(self):
        return reverse ("listProdutos", args=[self.slug])
    
    





class Entregador(models.Model):
    nome = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, help_text="EX.:nome-segundo")
    cpf = models.CharField(max_length=11, help_text="EX.: 99999999999")
    
    telefone1 = models.CharField(max_length=14, help_text="EX.:99999999999999")
    telefone2 = models.CharField(max_length=14, null=True, blank=True, help_text="EX.:9999999999999")

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name="get_entregador")
    img = models.ImageField(help_text="Tamanho máximo 50x50", verbose_name="Imagem", null = True, blank=True)

    endereco = models.ManyToManyField(Endereco)
    filiado = models.OneToOneField(Delivery, on_delete=models.PROTECT)
    placa_veiculo = models.CharField(max_length=8, verbose_name="Placa do Veículo", help_text="EX.: AAA-9999")


    class Meta:
        verbose_name_plural = "Entregadores"

    def __str__(self):
        return self.nome

class ProdutoPedido(models.Model):
    id_produto = models.IntegerField()
    id_pedido = models.IntegerField()
    quantidade_itens = models.IntegerField(verbose_name="Quantidade", null=True, blank=True)
class Pagamento(models.Model):

    STATUS_CHOICE = ( 
        ("1","Pagamento Pendente"),
        ("2","Pagamento Realizado"),
    )


    qntItensTotal = models.IntegerField(blank=True , null=True)
    status_pagamento = models.CharField(max_length=50, choices=STATUS_CHOICE, blank=True, null = True)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null = True)
class Pedido(models.Model):

    
    
    ENTREGA_CHOICE = (
        ("1", "Preparando"),
        ("2", "A Caminho"),
        ("3", "Entregue"),
    )

    entregador = models.ForeignKey(Entregador, on_delete = models.PROTECT, blank=True , null=True)
    status_pedido = models.BooleanField(default=False)  
    entrega = models.CharField(max_length=50, choices=ENTREGA_CHOICE)
    endereco_entrega = models.ManyToManyField(Endereco, blank=True , null=True)
    cliente = models.ForeignKey(Cliente,  blank=True, null = True, on_delete= models.PROTECT, related_name="getCliente")
    
    

    class Meta:
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return "Pedido: nº{}".format(self.pk)

class Produto(models.Model):

    CATEGORIA_CHOICE = (
        ("refeicao", "Refeição"),
        ("bebida", "Bebida"),
        ("sobremesas", "Sobremesa"),
    )

    nome = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    valor = models.DecimalField(decimal_places=2,max_digits=8)
    categoria_produto  = models.CharField(max_length=50, choices=CATEGORIA_CHOICE, verbose_name = "Categoria")
    observacoes = models.TextField()
    data_validade = models.DateTimeField()
    peso = models.DecimalField(decimal_places=3,max_digits=5, help_text="(g)")
    restaurante = models.ManyToManyField(Delivery, related_name="getDeliverys")
    id_produto_pedido = models.ForeignKey(ProdutoPedido, on_delete= models.PROTECT, blank=True, null  = True, related_name="getPedido")
    img = models.ImageField(help_text="Tamanho máximo 50x50", verbose_name="Imagem", null = True, blank=True)
    


    class Meta:
        verbose_name_plural = "Produtos"
        verbose_name = "Produto"

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse ("listProdutoDetail", args=[self.slug])



@receiver(post_save, sender = Produto)
def insert_slug_pruduto(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.nome)
        return instance.save()

@receiver(post_save, sender = Cliente)
def insert_slug_cliente(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.nome)
        return instance.save()

@receiver(post_save, sender = Delivery)
def insert_slug_delivery(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.nome_restaurante)
        return instance.save()

@receiver(post_save, sender = Entregador)
def insert_slug_entregador(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.nome)
        return instance.save()


