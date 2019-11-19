from django.contrib import admin

from .models import *

admin.site.register(Pessoa)
admin.site.register(Endereco)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(Empresa)