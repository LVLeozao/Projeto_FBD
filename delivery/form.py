from django.forms import ModelForm
from .models import Endereco, Usuario, Cliente, Delivery
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



class EnderecoForm(ModelForm):
    class Meta:
        model = Endereco
        fields = ("rua", "numero", "complemento", "bairro", "cidade", "estado","pais")

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ("telefone_1","telefone_2","img")

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ("nome","genero","cpf", "idade")

class DeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = ("nome_restaurante","cnpj","descricao")


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

    


