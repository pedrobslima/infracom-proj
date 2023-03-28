import socket
import os

HOST = "localhost"  # endereço IP do servidor (pode ser sla, 127.0.0.1)
PORT = 5000         # porta do servidor
orgn = (HOST, PORT) # vai servir para associar essa máquina ao cliente

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orgn)

print("Servidor: On\n")

dados = ''
while(dados != b'\x18'):
    dados, clientADDR = udp.recvfrom(1024) # buffer size is 1024 bytes
    print(clientADDR, dados.decode()) # o .decode() transforma o arquivo em bits em string
    if(dados.decode() == "1"):
        fileSize = os.stat("cardapio.txt").st_size # método para achar o tamanho em bytes do arquivo, mas como mandá-lo em pacotes de 1024 bytes?
        print(f"Size: {fileSize} bytes")
        file = open("cardapio.txt", "r")
        udp.sendto(file.encode(), ("localhost", 3000))
        # Obs.: O trecho a seguir, no futuro, deverá mandar o arquivo todo em pacotes de 1024 bytes
        # Obs.: Mandando em pacotes diferentes, será que deveria na verdade mandar o arquivo e depois abrir?
        #for line in file.readlines():
        #    udp.sendto(line.encode(), ("localhost", 3000))
        file.close()

print("\nServidor: Off\n")
udp.close() # num cenário real, não deve ser fechado o do servidor por comando do cliente,
# mas se a conexão udp não for fechada, vc precisa ir no taskmanager > detalhes
# e fechar tudo executando com o nome "py.exe" (não "python.exe")
