from django.views.generic import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.urls import reverse, reverse_lazy
from .form import *
from django.contrib.auth.models import User


class ListDeliveryView(ListView):
    model = Delivery
    template_name = "delivery/list_deliverys.html"
    context_object_name = "objects"


class ListProdutosDeliveryView(ListView):
    model = Produto
    template_name = "delivery/delivery_produtos_detail.html"
    context_object_name = "objects"


def list_deliverys(request):
    return render(request, "delivery/list_deliverys.html")


class CreateDeliveryView(CreateView):
    model = Delivery
    fields = "__all__"
    template_name = "delivery/criarDelivery.html"
    success_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        print(request.POST["nome_restaurante"])










def criarUsuarioView(request):
    array = {}
    endereco = EnderecoForm(request.POST or None)
    usuario = UsuarioForm(request.POST or None)
    cliente = ClienteForm(request.POST or None)
    user = UserCreationFormWithEmail(request.POST or None)

    array["endereco"] = endereco
    array["usuario"] = usuario
    array["cliente"] = cliente
    array["user"] = user

    if request.POST:

        # Endereco
        rua = request.POST['rua']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        pais = request.POST['pais']
        # Usuario
        telefone1 = request.POST["telefone_1"]
        telefone2 = request.POST["telefone_2"]
        imagem = request.POST["img"]
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

        try:
            objEndereco = Endereco.objects.get(rua=rua, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, estado=estado, pais=pais)
        except:
            objEndereco = Endereco(rua=rua, numero=numero, complemento=complemento,bairro=bairro, cidade=cidade, estado=estado, pais=pais)
            objEndereco.save()

        
        try:
            objUser =User.objects.get(username=username, password=password1, email=email)
        except:
            objUser = User(username=username, password=password1, email=email)
            objUser.save()
        
        try:
            objUsuario = Usuario.objects.get(telefone_1=telefone1, telefone_2=telefone2, user=objUser, img=imagem)
        except:
            objUsuario = Usuario(telefone_1=telefone1, telefone_2=telefone2, user=objUser, img=imagem)
            objUsuario.save()

        
        try:
            objCliente = Cliente.objects.get(nome=nome, genero=genero, cpf=cpf, idade=idade, usuario=objUsuario, endereco=objEndereco)
        except:
            
            objCliente = Cliente(nome=nome, genero=genero, cpf=cpf, idade=idade, usuario=objUsuario, endereco = objEndereco)
            objCliente.save()
        
        return redirect("login")

    else:

        return render(request,"delivery/cadastroCliente.html", array)




#  validarUser = verificar_user(username,password1, email)
#                 validarUsuario = verificar_usuario(telefone1, telefone2, imagem, validarUser)
#                 validarCliente = verificar_cliente(nome,genero,cpf,idade,validarEntedereco,validarUsuario)


