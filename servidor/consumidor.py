class Consumidor:

    def __init__(self,nome, mesa, ip, porta):
        self.nome = nome #nome do cliente
        self.mesa = mesa #mesa em que o cliente está
        self.ip = ip     #ip do cliente
        self.porta = porta #porta do clente
        self.pedidos = []  #lista de pedidos do cliente
        self.custo = 0     #quanto o cliente gastou ao total
        self.status_conta = False #se tá paga a conta ou não. True ->pago; False->Ainda não está pago


    def registrar_pedido(self, nome_prato, valor):
        novo_pedido =[] #esse novo pedido contém o nome do prato e valor
        novo_pedido.append(nome_prato)
        novo_pedido.append(valor)
        self.pedidos.append(novo_pedido) #adicionamos o pedido a lista de pedidos do nosso cliente
        self.custo += valor #acrescentamos no custo com esse novo pedido

    def get_conta_individual(self):
        #o output segue a estrutura que foi pedido na especificação do projeto
        #como o output contém várias linhas, criamos uma variável pra ir concatenando as várias frases

        output = f"| {self.nome} | \n \n " #primeira linha do output contendo o nome
        
        for i in self.pedidos:
            output += f"{i[0]} => {i[1]} \n" #sequência de linhas que vão conter todos os pratos pedidos e seus valors
        
        output += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n"

        output += f"Total - R$ {self.custo}\n"  #total gasto pelo cliente

        output += "-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n"

        return output

#essa função serve pra saber se o valor que o cliente está pagando é o correto ou excede
    def pagar_conta(self, valor_pago):
        if(valor_pago < self.custo):
            return "menor"
        
        elif(valor_pago == self.custo):
            self.custo = 0
            self.status = True #como o valor está correto, colocamos o status como True, ou seja, pago
            return "pago"
            
        else:
            self.status = True
            self.custo = 0
            return valor_pago - self.custo