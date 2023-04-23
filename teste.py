import socket
from math import ceil
import os
from funcoes import *
#socket.setdefaulttimeout(2)
# Para começar a fazer os testes, precisa 1o criar um novo terminal,
# e depois precisa clicar naquele simbolozinho de duas janelas na aba do terminal
# depois escreve "py servidor\server.py" em um e "py client.py" no outro
FILE_NAME = 'este.txt'
f = open(f"servidor//{FILE_NAME}", "rb")
f.close()

