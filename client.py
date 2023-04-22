import socket
from math import ceil
import os
from funcoes import *
socket.setdefaulttimeout(2)
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
    # ENVIAR O ARQUIVO:
    try:
        file = open(f"cliente//{file_name}", "rb")
        fileSize = os.stat(f"cliente//{file_name}").st_size 
        # ^ quantidade de bytes do arquivo
    except(FileNotFoundError or PermissionError):
        print("[ARQUIVO NÃO EXISTE]")
        continue
    num_pkts = ceil(fileSize/1024) # < o número de pacotes em q o arquivo será enviado, sem contar com a inicial
    #num_pkts = ceil(fileSize/1008)
    count = -1 # < '-1' por causa do pacote inicial
    sending = True
    half_one_or_zero = '0' # nome temporário
    while(sending):
        # WAIT STATE 0:
        while(True):
            # como fazer para receber pacotes aqui para que sejam ignorados?
            above_call = input(f"Pkt type {half_one_or_zero}: ")
            if(above_call == half_one_or_zero):
                count += 1
                break
        
        # SEND PACKET:
        if(count == 0):
            msg = (num_in_dec_num_bin_in_bin(num_pkts, "decimal") + file_name).encode()
            print('[Enviando pacote introdutório]')
        else:
            msg = file.read(1024)
            print(f'[Enviado pacote {count}/{num_pkts}]')
        #msg = '0'.encode() + data + checksum.encode()
        #^[1024] ^[- de 1]      ^[~1008]    ^[16]
        
        udp.sendto(msg, dest)

        # WAIT ACK 0:
        ACK_rcvd = False
        while(not(ACK_rcvd)):
            try:
                dados, serverADDR = udp.recvfrom(1024)
                ACK_rcvd = isntCorrupt(dados) and isACK(dados, half_one_or_zero)
            except(socket.timeout):
                print(f'[!!! Timer do ACK-{half_one_or_zero} estourado !!!]')
                print(f'[Re-enviando pacote {count}/{num_pkts}]')
                udp.sendto(msg, dest)

        # CHECK:
        half_one_or_zero = invertACK(half_one_or_zero)
        sending = count != num_pkts
    file.close()
    print('''_______________________________________
[ENVIO DE ARQUIVO: COMPLETO]
...
[AGUARDANDO RESPOSTA DO SERVIDOR...]
_______________________________________''')
    
    # RECEBER ARQUIVO E DUPLICAR: (ainda tá no início, vou dormir agr)
    count = 0
    ACK: int
    file_name = "copia_de_" + file_name
    copyFile = open(f"cliente//{file_name}", "wb")
    receiving = True
    while(receiving):
        dados, serverADDR = udp.recvfrom(1024)
        print(f'[Recebido pacote {count+1}/{num_pkts}]')
        if(ACK == half_one_or_zero):
            copyFile.write(dados)
            udp.sendto(ACK, dest)
    copyFile.close()

print("\nCliente: Off\n")
udp.close()
