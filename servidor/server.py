import socket
from math import ceil
import os
import time # vai usar para dar os waits(talvez) e para pegar a hora atual
import zlib # vai usar para o checksum
import struct# vai usar para o header em si do UDP 

def checksum_calculator(data):
    checksum = zlib.crc32(data)
    return checksum

HOST = "localhost"  # < endereço IP do servidor (127.0.0.1 é o padrão)
PORT = 5000         # < porta do servidor
orgn = (HOST, PORT) # < vai servir para associar essa máquina ao cliente
#dest = ("localhost", 3000) 
# ^ dps tem que tirar
porta_origem = 1111
porta_dest = 1112
comprimento = len(msg.encode())
checksum = checksum_calculator(msg.encode())
header_udp = struct.pack("!IIII", porta_origem, porta_dest, comprimento, checksum)



udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orgn)
# Ainda tecnicamente precisa fazer os passos iniciais da criação
# da conexão via UDP, do cliente pedindo para criar uma conexão com o server
print("Servidor: Stand by\n")

dados = ''
# Cada mensagem na vdd deverá ter 8128bits, ou seja, 1016 bytes
# por isso as partes retiradas do arquivo deverão ser de 1016 bytes
while(dados != b'\x18'): # < adicionar parte de "Levantar da mesa" e da comida paga (ou talvez quando o número de cliente for 0?)
    x = udp.recvfrom(1024)
    print(x)

    #unpacking header
    header_udp = x[:16] #metade só de header
    dados = x[16:] #metade só de dados

    dados, clientADDR = x # < tamanho do buffer é de 1024 bytes
    print(clientADDR, dados.decode()) # < o .decode() transforma o arquivo em bits em string
    # [adicionar condicional para saber se o clientADDR é do socket atual ou não]
    if(dados.decode() == "1" or dados.decode().capitalize() == "Cardárpio"):
        # v método para achar o tamanho em bytes do arquivo
        fileSize = os.stat("servidor//bigFile_teste.txt").st_size
        print(f"Size: {fileSize} bytes")
        # v definindo o número de pacotes que deverão ser enviados
        num_pkts = ceil(fileSize/1024)
        # v abrindo arquivo escolhido
        #file = open("servidor\cardapio.txt", "rb") # < mudar o nome da variável para 'cardapio' msm?
        file = open("servidor//bigFile_teste.txt", "rb")
        for i in range(num_pkts): # loop para envio de pacotes
            udp.sendto((str(i)).encode(), clientADDR) # < usado só para testes, diz qual o nº do pacote 
            udp.sendto(file.read(1024), clientADDR)   
            # ^ ao usar o método .read(), a própria posição do cursor no arquivo 
            # mudará automaticamente para a posição pertencente ao 1025º byte
            # e assim segue, de 1024 bytes por 1024 bytes
            # Obs.: Se você pedir para o código ler uma quant de bytes 
            # maior do que resta, não vai dar erro nenhum
        udp.sendto('file end'.encode(), clientADDR)
        # ^ é correto usar isso para sinalizar que o arquivo chegou ao seu fim?
        file.close() # < fechando arquivo

# v o ideal seria botar essas duas linhas assim que o cliente se levantasse da mesa (no loop)
print("\nServidor: Off\n")
udp.close() # < num cenário real, não deve ser fechado o do servidor por comando 
# do cliente, mas se a conexão udp não for fechada, vc precisa ir no 
# taskmanager > detalhes e fechar tudo executando com o nome "py.exe" (não "python.exe")
