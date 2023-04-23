import socket
from math import ceil
import os
from funcoes import *

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

print("Cliente: On\nPara sair use CTRL+X\n")
print('Formato do nome: "nome"."tipo"\n\tExp.: nome_imagem.jpg\n')

while True:
    file_name = input("[Cliente]: ") # < qual o nome.tipo do arquivo pra ser enviado
    
    if(file_name == '\x18'):
        udp.sendto(file_name.encode(), dest)
        break
    
    try:
        # ENVIAR
        file = open(f"cliente//{file_name}", "rb")
        fileSize = os.stat(f"cliente//{file_name}").st_size 
        # ^ quantidade de bytes do arquivo
        num_pkts = ceil(fileSize/1024) # < o número de pacotes em q o arquivo será enviado, sem contar com a inicial
        
        for i in range(num_pkts+1):
            if(i == 0):
                msg = (num_in_dec_num_bin_in_bin(num_pkts, "decimal") + file_name).encode()
                print('[Enviando pacote introdutório]')
            else:
                msg = file.read(1024)
                print(f'[Enviando pacote {i}/{num_pkts}]')
            
            udp.sendto(msg, dest) 
        file.close()

        # RECEBER E ARMAZENAR
        print('''_______________________________________
[ENVIO DE ARQUIVO: COMPLETO]
...
[AGUARDANDO RESPOSTA DO SERVIDOR...]
_______________________________________''')

        file_name = "copia_de_" + file_name
        copyFile = open(f"cliente//{file_name}", "wb")
        for i in range(num_pkts):
            dados, serverADDR = udp.recvfrom(1024)
            print(f'[Recebido pacote {i+1}/{num_pkts}]')
            copyFile.write(dados)

        copyFile.close()
        print(f'''_______________________________________
[RECEBIMENTO DE ARQUIVO: COMPLETO]
[CÓPIA DE ARQUIVO: COMPLETA]
_______________________________________''')
    except(FileNotFoundError or PermissionError):
        print("[ARQUIVO NÃO EXISTE]")

print("\nCliente: Off\n")
udp.close()
