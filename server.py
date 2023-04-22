import socket
from funcoes import *

ORGN_HOST = "localhost"  # < endereço IP do servidor (127.0.0.1 é o padrão)
ORGN_PORT = 5000         # < porta do servidor
orgn = (ORGN_HOST, ORGN_PORT) # < vai servir para associar essa máquina ao cliente

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orgn)

print("Servidor: On\n")

dados = ''
while True:
    # RECEBER E ARMAZENAR:
    dados, clientADDR = udp.recvfrom(1024)
    if(dados == b'\x18'):
        break
    

print("\nServidor: Off")
udp.close()