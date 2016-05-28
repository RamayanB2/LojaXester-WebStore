from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from decimal import Decimal
from .models import Produto,Usuario,Pedido
from .models import Carrinho
from .models import ItemProduto

def index(request):
    template = loader.get_template('ecommerce/index.html')
    search_tag = request.POST.get('search_tag')
    user_id = request.POST.get('us_id')
    user = Usuario.objects.get(id =user_id)

    if search_tag == None or search_tag == '':
        context = {  
            'usuario':user,      
            'produtos': Produto.objects.all(),
        }
    else:
        context = {    
            'usuario':user,      
            'produtos': Produto.objects.filter(nome__startswith=search_tag)
        }
    return HttpResponse(template.render(context, request))

 
def cart(request):
    template = loader.get_template('ecommerce/cart.html')
    user_id = request.POST.get('us_id')    
    if not user_id==None:
        user = Usuario.objects.get(id = user_id)
    total = Decimal(0.0)
    
    if Carrinho.objects.filter(usuario = user).exists():
        car = Carrinho.objects.last()
    else:
        car = Carrinho.objects.create(usuario = user,precoTotal = 0)
        total = 0
    car.save()

    if Pedido.objects.filter(carrinho = car).exists():
        car = Carrinho.objects.create(usuario = user,precoTotal = 0)
        total = 0
        car.save()

    context = {
            'usuario':user,
            'carrinho': car,
            'total':total,
    }
	
    for key in request.POST.keys():
        if key==('itemProduto_id'):
                
            print("Removendo")
            itemProduto_id = request.POST.get('itemProduto_id')
            item = ItemProduto.objects.get(id = itemProduto_id)    
            ItemProduto.objects.filter(id = itemProduto_id).delete();
	
            if not ItemProduto.objects.all():
                Carrinho.objects.all().delete()	
                print ('Carrinho vazio')				
	
        if key==('produto_id'):
            print("Entrou no adicionar")
            prod_id = request.POST.get(key)
            prod = Produto.objects.get(id=prod_id)

        

            if ItemProduto.objects.filter(produto_id = prod.id, carrinho_id = car.id).exists():
                item = ItemProduto.objects.get(produto=prod, carrinho = car)
                item.quantidade +=1
            else:
                item = ItemProduto.objects.create(produto=prod, 
                                                  quantidade=1, 
                                                  carrinho=car)                
            
            item.save()

    for item in ItemProduto.objects.filter(carrinho = car):
        total += item.produto.preco * item.quantidade

    car.precoTotal = total
    car.save()
    context = {
        'usuario':user,
        'carrinho': car, 
        'total' : total,
    }
    return HttpResponse(template.render(context, request))



def login(request):
    usuarioNome = request.POST.get('usuario_nome')    
    usuarioSenha = request.POST.get('usuario_senha')

    if Usuario.objects.filter(nome = usuarioNome,senha = usuarioSenha).exists():
        context = {
            'usuario':Usuario.objects.get(nome = usuarioNome,senha = usuarioSenha),
            'produtos': Produto.objects.all(),
        }
        template = loader.get_template('ecommerce/index.html')
        return HttpResponse(template.render(context, request))
    else:
        context = {
            'usuario':usuarioNome,
            'Senha':usuarioSenha,
        }
        template = loader.get_template('ecommerce/login.html')
        return HttpResponse(template.render(context, request))


def register(request): 
    template = loader.get_template('ecommerce/register.html') 

    N = request.POST.get('usuario_nome')    
    S = request.POST.get('usuario_senha')
    Em = request.POST.get('usuario_email')    
    End = request.POST.get('usuario_endereco')
    Cpf = request.POST.get('usuario_cpf')
    context={}
    if(N!=None and N!='' and S!='' and Em!='' and End!='' and Cpf!=''):
        newUser = Usuario.objects.create()
        newUser.nome = N
        newUser.senha = S
        newUser.email = Em
        newUser.endereco = End
        newUser.Cpf = Cpf
        newUser.save()
        template = loader.get_template('ecommerce/registerSucess.html')
        return HttpResponse(template.render(context, request))
        
    return HttpResponse(template.render(context, request))
    

def payment(request):
    template = loader.get_template('ecommerce/payment.html') 

    user_id = request.POST.get('us_id')    
    carrinho_id = request.POST.get('car_id')
    total = request.POST.get('tot')

    user = Usuario.objects.get(id =user_id)
    car = Carrinho.objects.get(id =carrinho_id)

    if not Pedido.objects.filter(carrinho = car).exists():
        ped = Pedido.objects.create(carrinho = car,total = total,status = 'pagamento em espera')
        ped.save()
    else:
        ped = Pedido.objects.get(carrinho=car)
        ped.save()

    context= {
        'pedido':ped,
        'carrinho':car,
    }

    return HttpResponse(template.render(context, request))


def meusPedidos(request):
    template = loader.get_template('ecommerce/meusPedidos.html') 

    user_id = request.POST.get('us_id')
    user = Usuario.objects.get(id =user_id)
    carrinhos_do_user = Carrinho.objects.filter(usuario = user)
    pedidos = set()

    for c in carrinhos_do_user:
        if Pedido.objects.filter(carrinho=c).exists():
            pedidos.add(Pedido.objects.get(carrinho = c))

    context ={
        'pedidos': pedidos,
        'usuario':user,
    }

    return HttpResponse(template.render(context, request))
