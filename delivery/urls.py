from . import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    
    path("accounts/criarDelivery/", views.criarDeliveryView, name="criarDelivery"),
    path("accounts/criarCliente/", views.criarClienteView, name="criarCliente"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("pedeMais/", views.HomeView, name = "home"),
    path('pedeMais/carrinho', views.CarrinhoDeliveryView, name="carrinhoView"),
    path('pedeMais/produto', views.ProdutoView.as_view(), name="produtoView"),
    path('pedeMais/produto/cadastroProduto', views.cadastroProduto.as_view(), name="cadastroProdutoView"),
    path("pedeMais/listDeliverys/", views.ListDeliveryView, name="listDeliverys"),
    path('pedeMais/listDeliverys/listProdutos/<slug:slug>/', views.ProdutosListView, name="listProdutos"),
    path('pedeMais/listDeliverys/listProdutos/detail/<slug:slug>/', views.ProdutoDetailView, name="listProdutoDetail"),
    
]
