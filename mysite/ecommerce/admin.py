from django.contrib import admin
from .models import Produto,Usuario,ItemProduto,Carrinho,Pedido,Estoque


admin.site.register(Usuario)
admin.site.register(Produto)
admin.site.register(ItemProduto)
admin.site.register(Carrinho)
admin.site.register(Pedido)
