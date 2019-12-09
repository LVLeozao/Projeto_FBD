from . import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/criarDelivery/", views.criarDeliveryView, name="criarDelivery"),
    path("accounts/criarCliente/", views.criarClienteView, name="criarCliente"),
    path("pedeMais/", views.HomeView, name = 'home'),
    path("pedeMais/delivery/produto", views.ProdutoView.as_view(), name = 'produtoView'),
    path("pedeMais/delivery/produto/cadastrarProduto", views.cadastroProduto, name = 'cadastroProduto'),
    
    path('pedeMais/carrinho/editarEndereco/<int:pk>', views.alterarEndereco, name="alterarEndereco"),
    path('pedeMais/carrinho/', views.CarrinhoDeliveryView, name="carrinhoView"),
    path('pedeMais/historicoPedido/', views.HistoricoPedidoView, name="historicoPedido"),
    path('pedeMais/carrinho/remover/<int:pk>/', views.removerItem, name = "excluir"),
    path("pedeMais/listDeliverys/", views.ListDeliveryView, name="listDeliverys"),
    path('pedeMais/listDeliverys/listProdutos/<slug:slug>/', views.ProdutosListView, name="listProdutos"),
    path('pedeMais/listDeliverys/listProdutos/detail/<slug:slug>/', views.ProdutoDetailView, name="listProdutoDetail"),
]

