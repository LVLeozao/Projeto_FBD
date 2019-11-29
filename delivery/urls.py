from . import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    
    #path("dashboard/", views.HomeView.as_view(), "home"),
    path("accounts/criarDelivery/", views.criarDeliveryView, name="criarDelivery"),
    path("accounts/criarCliente/", views.criarClienteView, name="criarCliente"),
    path("accounts/", include("django.contrib.auth.urls")),
    #path("accounts/criarDelivery/", views.CreateDeliveryView.as_view(), name="create_delivery"),
    path("pede-mais/list-deliverys/", views.ListDeliveryView.as_view(), name="deliverys"),
    
]
