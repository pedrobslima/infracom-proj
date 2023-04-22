import socket
from math import ceil
import os
from funcoes import *
#socket.setdefaulttimeout(2)
# Para começar a fazer os testes, precisa 1o criar um novo terminal,
# e depois precisa clicar naquele simbolozinho de duas janelas na aba do terminal
# depois escreve "py servidor\server.py" em um e "py client.py" no outro

DEST_HOST = "localhost"  # < endereço IP do servidor (127.0.0.1 é o padrão)
DEST_PORT = 5000         # < porta do servidor
dest = (DEST_HOST, DEST_PORT)
ORGN_HOST = "localhost"  # < endereço IP do cliente (127.0.0.1 é o padrão)
ORGN_PORT = 3000         # < porta do cliente
orgn = (ORGN_HOST, ORGN_PORT)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orgn)

udp.settimeout(2.0)
print(udp.gettimeout())
try:
    udp.recvfrom(1024)
except(socket.timeout):
    print("Erro de timeout")

udp.setblocking(True)

print(udp.gettimeout())
#print(socket.getdefaulttimeout())

udp.close()
