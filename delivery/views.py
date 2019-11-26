from django.views.generic import *
from .models import *
from django.shortcuts import render

class ListDeliveryView(ListView):
    model = Delivery    
    template_name = "delivery/list_deliverys.html"
    context_object_name = "objects"

class ListProdutosDeliveryView(ListView):
    model = Produto    
    template_name = "delivery/delivery_produtos_detail.html"
    context_object_name = "objects"



def home(request):
    return render(request, "delivery/home.html")

# def list_deliverys(request):
#     return render(request, "delivery/list_deliverys.html")


