from . import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    
    path("accounts/criarDelivery/", views.criarDeliveryView, name="criarDelivery"),
    path("accounts/criarCliente/", views.criarClienteView, name="criarCliente"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("pedeMais/", views.HomeView, name = "home"),
    path("pedeMais/listDeliverys/", views.ListDeliveryView.as_view(), name="listDeliverys"),
    
]
