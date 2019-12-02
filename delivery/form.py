from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



class EnderecoForm(ModelForm):
    class Meta:
        model = Endereco
        fields = ("rua", "numero", "complemento", "bairro", "cidade", "estado","pais")

    
    
class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ("nome","genero","cpf", "idade", "telefone1", "telefone2", "img")

        def clean_cliente(self):
            nome = self.cleaned_data.get("nome")
            genero = self.cleaned_data.get("genero")
            cpf = self.cleaned_data.get("cpf")
            idade = self.cleaned_data.get("idade")
            telefone1 = self.cleaned_data.get("telefone1")
            telefone2 = self.cleaned_data.get("telefone2")
            


            if Cliente.objects.filter(nome = nome, genero = genero, cpf = cpf, idade = idade, telefone1 = telefone1, telefone2 = telefone2).exists():
                raise forms.ValidationError("Cliente exsitente no banco de dados, tente novamente.")
        
            return nome, genero, cpf, idade, telefone1,telefone2

class DeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = ("nome_restaurante","cnpj","descricao", "telefone1", "telefone2", "img")

class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ("nome", "valor", "categoria_produto", "observacoes", "data_validade", "peso", "img")


class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Obrigatório")
    
    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
    
        return email

    


