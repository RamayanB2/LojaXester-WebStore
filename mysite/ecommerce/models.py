from django.db import models

#------------------------------------------------------------------------------

class Usuario(models.Model):    
    nome = models.CharField(max_length=40)
    email = models.EmailField(max_length=30)
    senha = models.CharField(max_length=20)
    cpf = models.CharField(max_length=11)
    endereco = models.CharField(max_length=100)

    def setSenha(self,newSenha):
        self.__senha = newSenha

    def getSenha(self):
        return self.__senha

    def setEmail(self,newE):
        self.__email = newE

    def setEndereco(self,newEnd):
        self.__endereco = newEnd

    def getEmail(self):
        return self.__email

    def getNome(self):
        return self.__nome

    def getType(self):
        return "Usuario"

    def comecarCompras(self):
        return Carrinho(self)

    def printUser(self):
        print ("Usuario %d:\n %s,%s,\n cpf: %s\n senha:%s \n mora em: %s\n" % (self.__numb, self.__nome,self.__email,self.__cpf,self.__senha,self.__endereco))

#------------------------------------------------------------------------------
        
class Produto(models.Model):
    """Essa classe Ã© um produto imaginÃ¡rio que sÃ³ representa os dados de um produto"""
    nome = models.CharField(max_length=20)
    preco = models.DecimalField(max_digits=6, decimal_places=2)   
    desc = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='produtos')
    qtdEst = models.IntegerField()

    def setPreco(self,p):
        if(p>0):
            self.preco = p

    def setQtd(self, qtd):
        self.qtdEst = qtd

    def setDescricao(self,d):
            self.desc = d

    def setUrlImg(self,i):
            self.photo = i

    def getUrlImg(self):
        return self.photo

    def getDescricao(self):
        return self.desc

    def getPreco(self):
        return self.preco

    def getNome(self):
        return self.nome

    def getQtd(self):
        return self.qtdEst

    def getType(self):
        return "Produto"

    def addQtd(self,qtd):
        if(qtd>=0):
            self.qtdEst=c

    def removeQtd(self,qtd):
        if(self.qtdEst - qtd>=0):
            self.qtdEst= c

    def emptyQtd(self):
        self.qtdEst=0

    def printProduto(self):
        print ("Produto %d:\n %s, %s cada,\n descricao: %s \n qtd em estoque: %d\n img:%s\n" % (self.nome,self.preco,self.descricao,self.qtdEst,self.photo))

#-------------------------------------------------------------------------------

class ItemProduto(models.Model):
    """Representa o produto que esta sendo adicionado no carrinho pelo cliente e sua qtd que se quer comprar,
    Encapsula acesso a um produto de carrinho para que seja tratado separadamente de um produto normal (ou seja de estoque)
    A quantidade de PRODUTO Carrinho Ã© a quantidade no carrinho em questao"""

    quantidade = models.IntegerField()
    produto = models.ForeignKey(
        'Produto',
        on_delete=models.CASCADE
    )
    carrinho = models.ForeignKey(
        'Carrinho',
        on_delete = models.CASCADE,
        related_name = 'itens',
    )

    def getType(self):
        return "ItemProduto"

    def addOneUnit(self):
        self.quantidade = self.quantidade + 1

    def removeOneUnit(self):
        self.quantidade = self.quantidader - 1

    def emptyCar(self):
        self.quantidade = 0

    def getQtdCar(self):
        return self.quantidade
    
#------------------------------------------------------------------------------

class Pedido(models.Model):
    """Um pedido Ã© a finalizaÃ§ao de uma compra via um carrinho por um usuario"""
    total = models.DecimalField(max_digits=7, decimal_places=2)
    data = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = models.CharField(max_length=20)
    carrinho = models.ForeignKey( 'Carrinho', on_delete=models.CASCADE, )

    def getTotal(self):
        return self.__total

    def getCod(self):
        return self.__codigo

    def getData(self):
        return self.__data

    def getStatus(self):
        return self.__status

    def setTotal(self, total):
        self.__total = total 

    def setStatus(self, status):
        self.__status = status
       
    def setData(self, data):
        self.__data = data

    def getType(self):
        return "Pedido"

#------------------------------------------------------------------------------
    
class Carrinho(models.Model):
    """Um carrinho guarda os produtos de um usuario especifico e modifica o preco total conforme mexe nos produtos(adcionar ou remover)"""
    precoTotal = models.DecimalField(max_digits=7, decimal_places=2)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, )
    
    def getProdutos(self):
        return self.__produtosNoCarrinho

    def verProdutos(self):
        for p in self.__produtosNoCarrinho:
            print("Produto: %s Quantidade: %d" % (p.getNome(), self.__produtosNoCarrinho[p]))

    def getUsuario(self):
        return self.__usuario

    def addProduto(self, produto, qtd):
        if(produto.getType()=="Produto"):
            if(produto in self.__produtosNoCarrinho):
                self.__produtosNoCarrinho[produto] = self.__produtosNoCarrinho[produto] + qtd
            else:
                self.__produtosNoCarrinho[produto] = qtd

            self.__precoTotal = self.__precoTotal + (produto.getPreco() * qtd)
        else:
            print("Produto deve ser do tipo Produto Carrinho")
     

    #Tem que checar se o produto esta no carrinho antes de remover, se nÃ£o buga
    def removeProduto(self, produto):
        if(produto.getType()=="ItemProduto"):
            if(produto in self.__produtosNoCarrinho):
                self.__precoTotal = self.__precoTotal - (produto.getPreco() * self.__produtosNoCarrinho[produto])
                del self.__produtosNoCarrinho[produto]
        else:
            print("Produto deve ser do tipo Produto Carrinho")

    
    def getType(self):
        return "Carrinho"

#-------------------------------------------------------------------------------

class Estoque(models.Model):
    """Estoque guarda todos os produtos possiveis, se o produto nao estiver em estoque quer dizer q a loja nao trabalha com esse produto"""
    produtos = {}
    produtosDisponiveis = set()

    def getProdutos(self):
        return self.__produtos

    def cadastraProduto(self, produto):
        self.__produtosDisponiveis.add(produto)

    def excluirProduto(self, produto):
        self.__produtosDisponiveis.discard(produto)

    def addProduto(self, produto, qtd):
        if(qtd > 0):
            if(produto in self.__produtosDisponiveis):
                self.__produtos[produto] = self.__produtos[produto] + qtd
                BancoDeDados.acrescentarNoEstoque(produto,qtd)
            else: 
                print("favor cadastrar produto")
            

    def removeProduto(self, produto, qtd):
        if(qtd > 0):
            if(produto in __produtosDisponiveis):
                self.__produtos[produto] = self.__produtos[produto] - qtd
                BancoDeDados.removerDoEstoque(produto, qtd)
            else: 
                print("favor cadastrar produto")

    def atualizaEstoque(self):
        self.__produtos = BancoDeDados.getEstoque()


    def print(self):
        for p in self.__produtos:
            p.printProduto()


    #Tem que checar se o produto esta no carrinho antes de remover, se nÃ£o buga
    def removeProduto(self, produto, qtd):
        if(produto in self.__produtos):
            if(self.__produtos[produto] <= qtd):
                del self.__produtos[produto]
                BancoDeDados.setProduto(produto, 0)
            else:
                self.__produtos[produto] = self.__produtos[produto] - qtd
                BancoDeDados.setProduto(produto, self.__produtos[produto]) 



