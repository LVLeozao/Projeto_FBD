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
    for x in produtos:
        valorTotal+=(x.valor*x.qnt)
        qntTotal+=x.qnt
    
    return valorTotal,  qntTotal

    
    

def PedidoDeliveryView(request):
    template_name = "delivery/carrinho.html"
    array={}
    array['type'] = getGroup(request.user.pk)

    
    

    return render(request, template_name, array)





        

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
    array["objects"] = Produto.objects.get(slug = slug)
    array['type'] = getGroup(request.user.pk)

    if request.POST:

        cliente = request.user.getCliente.first()
        
        pedidoAtivo = Pedido.objects.filter(status_pedido=False, cliente = cliente).first()

        if pedidoAtivo is not None:
            produto = Produto.objects.get(slug = slug)
            produto_pedido = ProdutoPedido(id_produto = produto, id_pedido = pedidoAtivo, quantidade_itens = request.POST['qnt'])
            
        else:


            pedidoNovo = Pedido(cliente = cliente, status_pedido=False)
            pedidoNovo.save()

            produto = Produto.objects.get(slug = slug)
            produto_pedido = ProdutoPedido(id_produto = produto, id_pedido = pedidoNovo, quantidade_itens = request.POST['qnt'])

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




