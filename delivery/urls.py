from . import views
from django.urls import path,include



urlpatterns = [
    
    #path("dashboard/", views.HomeView.as_view(), "home"),
    #path("accounts/", include("django.contrib.auth.urls")),
    path("pede-mais/home/", views.home, name="home"),
    path("pede-mais/list-deliverys/", views.ListDeliveryView.as_view(), name="deliverys")
    
    
]
