import socket
from math import ceil
import os
import time # vai usar para dar os waits(talvez) e para pegar a hora atual
import json
from consumidor import Consumidor
#from statemachine import State, StateMachine

HOST = "localhost"  # < endereço IP do servidor (127.0.0.1 é o padrão)
PORT = 5000         # < porta do servidor
orgn = (HOST, PORT) # < vai servir para associar essa máquina ao cliente
#dest = ("localhost", 3000) 
# ^ dps tem que tirar

clientes = {} #aqui é onde será armanezados todos os clientes conectados ao servidor 
mesas = {} #esse dicionário serve para agrupar os clientes por mesa
cliente = None
menu = ""
cardapio = {"arroz":5.00, "feijão":2.00, "batata":10.00}

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orgn)
# Ainda tecnicamente precisa fazer os passos iniciais da criação
# da conexão via UDP, do cliente pedindo para criar uma conexão com o server
print("Servidor: Stand by\n")

dados_decodados = ''
# ESTADO 0 (fazer os estados usando funções?)
#def Standby():
while(dados_decodados.capitalize() != "Chefia"):
    dados, clientADDR = udp.recvfrom(1024) 
    dados_decodados = dados.decode() #

    if(dados_decodados.capitalize() == "Chefia"):
        mesa_print = 'Digite sua mesa:'
        udp.sendto(mesa_print.encode(), clientADDR)
        cliente_mesa, clientADDR = udp.recvfrom(1024) #recebe a mesa
        nome_print = 'Digite seu nome'
        udp.sendto(nome_print.encode(), clientADDR)
        cliente_nome, clientADDR = udp.recvfrom(1024) #recebe nome
        opcao_print = 'Digite uma das opcoes'
        udp.sendto(opcao_print.encode(), clientADDR) #recebe a primeira ação do cliente
        cliente = Consumidor(cliente_nome, cliente_mesa, clientADDR, 3000) #registra o cliente na classe
        clientes[cliente_nome] = cliente #registra o cliente no dicionario de clientes

        if(cliente_mesa in mesas):
            mesas[cliente_mesa].append(cliente) #se a mesa já tiver no dicionário, adiciono esse novo cliente à lista de clientes
        else:
        #se não tive salva a mesa, criamos ela 
            lista_clientes = [] #criamos a lista de cliente pra salvar no valor do dicionario corresponde àquela mesa
            lista_clientes.append(cliente) #adicionamos o cliente a lista
            mesas[cliente_mesa] = lista_clientes #adicionamos a nova mesa no dic
       
        
        # [agora aqui precisaria adicionar as info coletadas no arquivo json]
        print("Servidor: On\n")

# ESTADO 1 (fazer os estados usando funções?)
#def Main():
while(dados != b'\x18'): # < adicionar parte de "Levantar da mesa" e da comida paga (ou talvez quando o número de cliente for 0?)
    dados, clientADDR = udp.recvfrom(1024) # < tamanho do buffer é de 1024 bytes
    print(clientADDR, dados.decode()) # < o .decode() transforma o arquivo em bits em string
    # [adicionar condicional para saber se o clientADDR é do socket atual ou não]
    if(dados.decode() == "1" or dados.decode().capitalize() == "Cardapio"):
        # v método para achar o tamanho em bytes do arquivo
        #fileSize = os.stat("servidor\cardapio.txt").st_size
        #print(f"Size: {fileSize} bytes")
        # v definindo o número de pacotes que deverão ser enviados
        #num_pkts = ceil(fileSize/1024)
        # v abrindo arquivo escolhido
        #file = open("servidor\cardapio.txt", "rb") # < mudar o nome da variável para 'cardapio' msm?
        #file = open("servidor\bigFile_teste.txt", "rb")
        tam_cardapio = str(len(cardapio.items()))
        udp.sendto(tam_cardapio.encode(), clientADDR) #envia o tamanho do cardapio para o cliente fazer o laço de recebimentos
        for chave, valor in cardapio.items(): 
                item = f"{chave} => R$ {valor}\n"
                udp.sendto(item.encode(), clientADDR) #envia cada item do cardapio para o cliente para ser impresso


        #for i in range(num_pkts): # loop para envio de pacotes
            #udp.sendto((str(i)).encode(), clientADDR) # < usado só para testes, diz qual o nº do pacote 
            #udp.sendto(file.read(1024), clientADDR)   
            # ^ ao usar o método .read(), a própria posição do cursor no arquivo 
            # mudará automaticamente para a posição pertencente ao 1025º byte
            # e assim segue, de 1024 bytes por 1024 bytes
            # Obs.: Se você pedir para o código ler uma quant de bytes 
            # maior do que resta, não vai dar erro nenhum
        #udp.sendto('file end'.encode(), clientADDR)
        # ^ é correto usar isso para sinalizar que o arquivo chegou ao seu fim?
        #file.close() # < fechando arquivo

    if(dados.decode() == "2" or dados.decode().capitalize() == "Pedido"):
        udp.sendto(b'Digite qual o item que voce gostaria', clientADDR)
        cliente_pedido, clientADDR = udp.recvfrom(1024) #recebe pedido
        cliente.registrar_pedido(cliente_pedido.decode(), cardapio[cliente_pedido.decode()]) #pedido do cliente é registrado

    if (dados.decode() == '3' or dados.decode().capitalize() == 'Conta individual'):
        udp.sendto(cliente.get_conta_individual().encode(), clientADDR) #envia a conta individual

    if dados.decode() == '4' or dados.decode().capitalize() == 'Conta da mesa':
        total_mesa_pagar = 0 #variável pra ir somando o custo dos clientes

        clientes_mesa = mesas[cliente.mesa] #aqui pegamos a lista de clientes da mesa em que o usuário está
        tam_mesa = str(len(cliente_mesa)) #tamanho do cardapio para o cliente fazer o laço de recebimentos
        udp.sendto(tam_mesa.encode(), clientADDR)
        
        for consumidor in clientes_mesa: #percorremos essa lista. Consumidor vai ser a variável que vai armazenar cada objeto cliente dessa lista
            total_mesa_pagar += consumidor.custo #vamos somando o custo total de todos daquela  mesa
            udp.sendto(cliente.get_conta_individual().encode(), clientADDR)

        total = (f"Total da mesa - R$ {total_mesa_pagar}") #printamos o valor total
        udp.sendto(total.encode(), clientADDR) 
            

    if (dados.decode() == '5' or dados.decode().capitalize() == 'Pagar'):
        conta = f'Sua conta foi {int(cliente.custo)}. Digite o valor a ser pago' 
        udp.sendto(conta.encode(), clientADDR) # manda o valor a ser pago
        valor, clientADDR = udp.recvfrom(1024) #recebe o valor que o cliente deseja pagar
        pago = cliente.pagar_conta(int(valor.decode())) #faz o calculo do valor pago com a conta
        if pago == 'menor':
            resposta = 'O valor nao e suficiente para pagar a conta'
            udp.sendto(resposta.encode(), clientADDR) #o cliente ainda não pode levantar
        elif pago == 'pago':
            resposta = 'Voce pagou sua conta, obrigado!'
            udp.sendto(resposta.encode(), clientADDR) #altera o status do cliente para que possa levantar
        else: #quando o valor for maior que o da conta
            pago = f'Voce está pagando {pago} a mais que a sua conta. O valor excedente será distribuído para os outros clientes'
            udp.sendto(pago.encode(), clientADDR) 

    if dados.decode() == '6' or dados.decode().capitalize() == 'Levantar':
        if cliente.status_conta: #checa se o cliente pagou 
            udp.sendto(b'Volte sempre!', clientADDR)
        else:
            udp.sendto(b'Voce ainda nao pagou sua conta', clientADDR)

# v o ideal seria botar essas duas linhas assim que o cliente se levantasse da mesa (no loop)
print("\nServidor: Off\n")
udp.close() # < num cenário real, não deve ser fechado o do servidor por comando 
# do cliente, mas se a conexão udp não for fechada, vc precisa ir no 
# taskmanager > detalhes e fechar tudo executando com o nome "py.exe" (não "python.exe")
