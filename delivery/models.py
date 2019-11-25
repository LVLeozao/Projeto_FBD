from django.db import models
from django.contrib.auth.models import User

class Endereco(models.Model):
    rua = models.CharField(max_length=200)
    numero = models.IntegerField(verbose_name = "Número")
    complemento = models.CharField(max_length=200)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=100)
    pais = models.CharField(max_length=2, help_text="EX.: BR", verbose_name = "País")

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
    restaurante = models.ManyToManyField("Delivery")
    pedido = models.ManyToManyField("Pedido", blank=True)
    #img = models.ImageField()

    class Meta:
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome

    def get_pk(self):
        return self.pk

class Usuario(models.Model):
    telefone_celular = models.CharField(max_length=14, help_text="EX.:99999999999999")
    telefone_fixo = models.CharField(max_length=13, null=True, blank=True, help_text="EX.:9999999999999")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    

class Cliente(models.Model):

    GENERO_CHOICES = (
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("O", "Outro"),
    )

    nome = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, help_text="EX.:nome-sobrenome")
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    cpf = models.CharField(max_length=11, help_text="EX.: 99999999999")
    idade = models.IntegerField()
    usuario = models.OneToOneField(Usuario, null=True, blank=True, on_delete=models.PROTECT) 
    endereco = models.ManyToManyField(Endereco)
    
    



class Delivery(models.Model):
    nome_restaurante = models.CharField(max_length=100, help_text="Nome do Delivery: ")
    usuario = models.OneToOneField(Usuario, null=True, blank=True, on_delete=models.PROTECT) 
    cnpj = models.CharField(max_length=18, help_text="99.999.999/9999-99", verbose_name="CNPJ")
    endereco = models.OneToOneField(Endereco, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    
    entregador = models.OneToOneField("Entregador", on_delete=models.PROTECT)
    pagamento = models.OneToOneField("Pagamento", on_delete = models.PROTECT)
    quantidade_itens = models.IntegerField(null=True, blank=True)
    pagamento = models.OneToOneField("Pagamento", on_delete=models.PROTECT, null=True, blank=True)
    #endereco_entrega = 

class Pagamento(models.Model):

    STATUS_CHOICE = ( 
        ("1","Pagamento Pendente"),
        ("2","Pagamento Realizado"),
    )
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE)

class Entregador(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, help_text="EX.: 99999999999")
    usuario = models.OneToOneField(Usuario, null=True, blank=True, on_delete=models.PROTECT) 
    endereco = models.OneToOneField(Endereco, on_delete=models.PROTECT)
    placa_veiculo = models.CharField(max_length=8, verbose_name="Placa do Veículo", help_text="EX.: AAA-9999")


