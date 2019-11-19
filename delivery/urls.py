from . import views
from django.urls import path,include


urlpatterns = [
    #path("teste/", views.DeliveryLoginView.as_view(), "login"),
    path("accounts/", include("django.contrib.auth.urls"))

]
