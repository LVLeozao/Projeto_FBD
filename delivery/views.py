from django.views.generic import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.urls import reverse, reverse_lazy
from .form import *
from django.http import HttpResponse

from django.contrib.auth.models import User



def getGroup(pk):
    grupo = User.objects.get(id = pk).groups.all().first().__str__()

    return "c" if grupo == "Clientes" else "d"

def calcularValor(produtos):
    valorTotal = 0
    qntTotal = 0

    for produto in produtos:
        
        valorTotal += (produto.id_produto.valor * produto.quantidade_itens)
        qntTotal+=produto.quantidade_itens
    
    return valorTotal,  qntTotal

    
    

def CarrinhoDeliveryView(request):
    pedidoAtivo = Pedido.objects.filter(status_pedido=False).first()
    array={}

    if pedidoAtivo is not None:
        objects = ProdutoPedido.objects.filter(id_pedido = pedidoAtivo).all()
        cliente = request.user.getCliente.first()
        
        if pedidoAtivo.endereco_entrega is None:
            endereco_entrega = request.user.getCliente.first().endereco.first()
        else:
            endereco_entrega = pedidoAtivo.endereco_entrega

        valorTotal, qntTotal =  calcularValor(objects)
        

        array['type'] = getGroup(request.user.pk)
        array['existePedido'] = 'true'
        array['objects'] = objects
        array["cliente"] = cliente
        array['enderecoEntrega'] = endereco_entrega
        array['valor'] = valorTotal
        array['qnt'] = qntTotal
        array['pk'] = pedidoAtivo.pk
        array['end'] = EnderecoForm
    
    elif Pedido.objects.filter(entrega__lt =3).first() is not None:
        array['existePedido'] = 'false'
        array['type'] = getGroup(request.user.pk)

        pedidoAtivo = Pedido.objects.filter(entrega__lt =3).first()

        
        array['acompanhamentoEntregador'] = "A definir" if pedidoAtivo.entregador == None else pedidoAtivo.entregador
        array['acompanhamentoStatus'] = "Preparando" if pedidoAtivo.status_pedido == 1 else "A Caminho"
        array['acompanhamentoEndereco'] = pedidoAtivo.endereco_entrega
        array['acompanhamentoCliente'] = pedidoAtivo.cliente
        array['acompanhamentoPendente'] = "Pendente"
    
    else:
        array['type'] = getGroup(request.user.pk)
        array['mensagem'] = "True"




    if request.POST:

        pedidoAtivo.status_pedido = True
        pedidoAtivo.entrega = 1
        pedidoAtivo.save()

        return redirect("home")



    return render(request, "delivery/carrinho.html", array)



def alterarEndereco(request, pk):
    template_name = "delivery/editarEndereco.html"
    
    array = {}
    array['objects'] = EnderecoForm
    array['type'] = getGroup(request.user.pk)
    
    if request.POST:

        rua = request.POST['rua']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        pais = request.POST['pais']

        objEndereco = Endereco.objects.filter(rua=rua, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, estado=estado, pais=pais).first()
        objPedido = Pedido.objects.filter(status_pedido=False).first()
        
        if objEndereco is not None:
            objPedido.endereco_entrega = objEndereco
            objPedido.save()
        
        else:
            objEndereco = Endereco(rua=rua, numero=numero, complemento=complemento,bairro=bairro, cidade=cidade, estado=estado, pais=pais)
            objEndereco.save()

            objPedido.endereco_entrega = objEndereco
            objPedido.save()

        return redirect("carrinhoView")
        



    return render(request,template_name, array)

        

def ListDeliveryView(request):
    array = {}
    array["objects"] = Delivery.objects.all()
    array['type'] = getGroup(request.user.pk)
    array['erro'] = "false"
    array["buscar_cidade"] = "true"
    template_name = "delivery/listDeliverys.html"

    if request.POST:
        
        

        try:

            endereco = Endereco.objects.filter(cidade = request.POST["cidade"] , estado = request.POST["estado"]).all()
            querys = []
            rest = []

            for end in endereco:
                querys.append(end)
                    
            for query in querys:
                for x in query.getEnderecos.all():
                    rest.append(x)

            array["objects"] = rest


            

        except:

            array["objects"] = Delivery.objects.all()
                          
            array['erro'] = "true"


        return render(request, template_name, array)
                


    return render(request, template_name, array)
    


def ProdutosListView(request, slug):
    template_name = "delivery/listProdutos.html"
    array = {}
    
    
    array["objects"] = Delivery.objects.get(slug=slug).getDeliverys.all()
    array['type'] = getGroup(request.user.pk)

    

    return render(request, template_name, array)


def HomeView(request):
        user = User.objects.get(id = request.user.pk)
        cliente = user.getCliente.all().first()
        array = {}
        array["cliente"] = cliente
        array['type'] = getGroup(request.user.pk)
        return render(request, "delivery/home.html", array)
    
class cadastroProduto(CreateView):
    model = Produto
    template_name = "delivery/cadastroProduto.html"
    success_url = reverse_lazy("home")

class ProdutoView(TemplateView):
    template_name = "delivery/viewProduto.html"


def ProdutoDetailView(request, slug):
    template_name = "delivery/listProdutoDetail.html"
    array = {}
    produto = Produto.objects.get(slug = slug)
    array["objects"] = produto
    array['type'] = getGroup(request.user.pk)

    if request.POST:

        cliente = request.user.getCliente.first()
        pedidoAtivo = Pedido.objects.filter(status_pedido=False, cliente = cliente).first()
        restaurante = produto.restaurante.first()
        if pedidoAtivo is not None:
            produto = Produto.objects.get(slug = slug)
            produto_pedido = ProdutoPedido(id_produto = produto, id_pedido = pedidoAtivo, id_delivery = restaurante , quantidade_itens = request.POST['qnt'])
            produto_pedido.save()
            
        else:
            pedidoNovo = Pedido(cliente = cliente, status_pedido=False)
            pedidoNovo.save()
            restaurante = produto.restaurante.first()
            produto = Produto.objects.get(slug = slug)
            produto_pedido = ProdutoPedido(id_produto = produto, id_pedido = pedidoNovo, id_delivery = restaurante, quantidade_itens = request.POST['qnt'])
            produto_pedido.save()

        return redirect("carrinhoView")
            
    return render(request, template_name, array)
    

def criarDeliveryView(request):
    array = {}
    endereco = EnderecoForm(request.POST or None)
    delivery = DeliveryForm(request.POST or None)
    user = UserCreationFormWithEmail(request.POST or None)

    array["endereco"] = endereco
    array["delivery"] = delivery
    array["user"] = user
    array["erro"] = False
    array["mensagem"] = ""

    if request.POST:
        array["erro"] = False
        array["mensagem"] = ""

        # Endereco
        rua = request.POST['rua']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        pais = request.POST['pais']
        # User
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]
        #Delivery
        nome_restaurante = request.POST["nome_restaurante"]
        cnpj = request.POST["cnpj"]
        descricao  = request.POST["descricao"]
        telefone1 = request.POST["telefone1"]
        telefone2 = request.POST["telefone2"]
        imagem = request.POST["img"]


        
        objEndereco = Endereco.objects.filter(rua=rua, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, estado=estado, pais=pais).first()
        objUser = User.objects.filter(username=username, password=password1, email=email).first()


        if(objEndereco is None):
            objEndereco = Endereco(rua=rua, numero=numero, complemento=complemento,bairro=bairro, cidade=cidade, estado=estado, pais=pais)
            objEndereco.save()

        
        if(objUser is None):
            objUser = User(username=username, password=password1, email=email)
            objUser.save()
        else:
            array["erro"] = True
            array["mensagem"] = "Usuário existente, tente novamente."
            return render(request,"delivery/cadastroCliente.html", array)



        objDelivery =  Delivery.objects.filter(nome_restaurante=nome_restaurante, cnpj = cnpj, user=objUser, endereco=objEndereco , descricao = descricao).first()

        if(objDelivery is None):

            objDelivery = Delivery(nome_restaurante=nome_restaurante, descricao = descricao, cnpj = cnpj, user=objUser, telefone1 = telefone1, telefone2 = telefone2, img = imagem)
            objDelivery.save()
            objDelivery.endereco.add(objEndereco)
        else:
            
            array["erro"] = True
            array["mensagem"] = "Cliente existente, tente novamente."
            return render(request,"delivery/cadastroCliente.html", array)


    
        
        return redirect("login")
    
    else:
        return render(request,"delivery/cadastroDelivery.html", array)
        
def criarClienteView(request):
    array = {}
    endereco = EnderecoForm(request.POST or None)
    cliente = ClienteForm(request.POST or None)
    user = UserCreationFormWithEmail(request.POST or None)

    array["endereco"] = endereco
    array["cliente"] = cliente
    array["user"] = user
    array["erro"] = False
    array["mensagem"] = ""
    

    if request.POST:

        array["erro"] = False
        array["mensagem"] = ""

        # Endereco
        rua = request.POST['rua']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        pais = request.POST['pais']
        # User
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]
        # Cliente
        nome = request.POST["nome"]
        genero = request.POST["genero"]
        cpf = request.POST["cpf"]
        idade = request.POST["idade"]
        telefone1 = request.POST["telefone1"]
        telefone2 = request.POST["telefone2"]
        imagem = request.POST["img"]


        objEndereco = Endereco.objects.filter(rua=rua, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, estado=estado, pais=pais).first()
        objUser = User.objects.filter(username=username, password=password1, email=email).first()


        if(objEndereco is None):
            objEndereco = Endereco(rua=rua, numero=numero, complemento=complemento,bairro=bairro, cidade=cidade, estado=estado, pais=pais)
            objEndereco.save()

        
        if(objUser is None):
            objUser = User(username=username, password=password1, email=email)
            objUser.save()
        else:
            array["erro"] = True
            array["mensagem"] = "Usuário existente, tente novamente."
            return render(request,"delivery/cadastroCliente.html", array)
    

        objCliente =  Cliente.objects.filter(nome=nome, genero=genero, cpf=cpf, idade=idade, user=objUser, endereco=objEndereco).first()

        if(objCliente is None):

             

            objCliente = Cliente(nome=nome, genero=genero, cpf=cpf, idade=idade, user=objUser, telefone1 = telefone1, telefone2 = telefone2, img = imagem)
            objCliente.save()
            objCliente.endereco.add(objEndereco)
        else:
            
            array["erro"] = True
            array["mensagem"] = "Cliente existente, tente novamente."
            return render(request,"delivery/cadastroCliente.html", array)
        
        return redirect("login")

    else:

        return render(request,"delivery/cadastroCliente.html", array)


def removerItem(request, pk):
    template_name = "delivery/carrinho.html"
    objects = ProdutoPedido.objects.get(id = pk)    
    objects.delete()

    return redirect("carrinhoView")

def HistoricoPedidoView(request):
    array = {}
    array['type'] = getGroup(request.user.pk)

    cliente = request.user.getCliente.first()
    pedidos = cliente.getCliente.all()


    array['objects'] = pedidos


    return render(request, 'delivery/historicoPedidos.html', array)


