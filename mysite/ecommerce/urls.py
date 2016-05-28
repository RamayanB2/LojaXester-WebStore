from django.conf.urls import url
from . import views

urlpatterns = [    
    url(r'^home/payment/', views.payment),
    url(r'^home/carrinho/', views.cart),
    url(r'^home/pedidos/', views.meusPedidos),
    url(r'^home/', views.index),    
    url(r'^$', views.login),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    
]

