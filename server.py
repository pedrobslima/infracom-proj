import socket
from math import ceil
import os

HOST = "localhost"  # endereço IP do servidor (127.0.0.1 é o padrão)
PORT = 5000         # porta do servidor
orgn = (HOST, PORT) # vai servir para associar essa máquina ao cliente
dest = ("localhost", 3000)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orgn)

print("Servidor: On\n")
# Ainda tecnicamente precisa fazer os passos iniciais da criação
# da conexão via UDP, do cliente pedindo para criar uma conexão com o server
dados = ''
while(dados != b'\x18'):
    dados, clientADDR = udp.recvfrom(1024) # buffer size is 1024 bytes
    print(clientADDR, dados.decode()) # o .decode() transforma o arquivo em bits em string
    if(dados.decode() == "1"):
        fileSize = os.stat("cardapio.txt").st_size # método para achar o tamanho em bytes do arquivo, mas como mandá-lo em pacotes de 1024 bytes?
        print(f"Size: {fileSize} bytes")
        num_pkts = ceil(fileSize/1024)
        file = open("cardapio.txt", "rb")
        for i in range(num_pkts):
            udp.sendto(file.read(1024), dest)   
            # ao usar o método .read(), a própria posição do cursor no arquivo 
            # mudará automaticamente para a posição pertencente ao 1025º byte
            # e assim segue, de 1024 bytes por 1024 bytes
            # Obs.: Se você pedir para o código ler uma quant de bytes 
            # maior do que resta, não vai dar erro nenhum
        file.close()
        # Obs.: O trecho a seguir, no futuro, deverá mandar o arquivo todo em pacotes de 1024 bytes
        # Obs.: Mandando em pacotes diferentes, será que deveria na verdade mandar o arquivo e depois abrir?
        #for line in file.readlines():
        #    udp.sendto(line.encode(), ("localhost", 3000))

print("\nServidor: Off\n")
udp.close() # num cenário real, não deve ser fechado o do servidor por comando do cliente,
# mas se a conexão udp não for fechada, vc precisa ir no taskmanager > detalhes
# e fechar tudo executando com o nome "py.exe" (não "python.exe")
