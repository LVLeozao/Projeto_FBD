from . import views
from django.urls import path,include




urlpatterns = [
    
    #path("dashboard/", views.HomeView.as_view(), "home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/criar", views.criarUsuarioView, name="criarCliente"),
    #path("accounts/criarDelivery/", views.CreateDeliveryView.as_view(), name="create_delivery"),
    path("pede-mais/list-deliverys/", views.ListDeliveryView.as_view(), name="deliverys"),
    
]
