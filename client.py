import socket
from math import ceil
import os
import time # vai usar para dar os waits(talvez) e para pegar a hora atual
import zlib # vai usar para o checksum
import struct# vai usar para o header em si do UDP 

def access_bit(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] >> shift) & 0x1

def byte_to_bit(x):
    y = ''
    for i in range(0, len(x)*8, 8):
        temp = ''
        for j in range(i, i+8):
            temp = str(access_bit(x, j)) + temp
        y = y + temp
    return y

def num_byte_to_num_bin_in_bin(x: int): # < working title
    x *= 8 # < num de bits em decimal
    soma = ''
    for i in range(15, -1, -1):
        div = 2**i
        if(x > div):
            soma = soma + '1'
            x = x % div
        else:
            soma = soma + '0'
    return soma

# Para começar a fazer os testes, precisa 1o criar um novo terminal,
# e depois precisa clicar naquele simbolozinho de duas janelas na aba do terminal
# depois escreve "py servidor\server.py" em um e "py client.py" no outro

file_name = ''

def checksum_calculator(data):
    checksum = zlib.crc32(data) #data entra, e usamos a biblioteca para gerar seu checksum
    return checksum

DEST_HOST = "localhost"  # < endereço IP do servidor (127.0.0.1 é o padrão)
DEST_PORT = 5000         # < porta do servidor
dest = (DEST_HOST, DEST_PORT)
ORGN_HOST = "localhost"  # < endereço IP do cliente (127.0.0.1 é o padrão)
ORGN_PORT = 3000         # < porta do cliente
orgn = (ORGN_HOST, ORGN_PORT)
#info = ORGN_HOST + ' ' + str(ORGN_PORT)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orgn)

print("Cliente: On\nPara sair use CTRL+X\n")

while(file_name != '\x18'):
    file_name = input("[Cliente]: ") # < qual o nome.tipo do arquivo pra ser enviado
    # Definir maneira de especificar o tipo do arquivo
    fileEnd = False # < indicará quando o arquivo terminou para parar o loop de recebimento
    #if(msg.capitalize() == "Chefia"):
    #    for i in range(2): 
    #        dados, serverADDR = udp.recvfrom(1024)
    #        print(f"[CINtofome]: {dados.decode()}")
    #        msg = input("[Cliente]: ")
    #        udp.sendto(msg_headed, dest)
    try:
        file = open(f"cliente//{file_name}", "rb")
        fileSize = os.stat(f"cliente//{file_name}").st_size 
        # ^ unidade em bytes
        num_pkts = ceil((fileSize+2)/1016)
                                # ^ o +2 serão os dois bytes do primeiro pacote 
                                # que indicarão o tamanho total do arquivo
        for i in range(num_pkts):
            if(i == 0):
                #msg = num_byte_to_num_bin_in_bin(fileSize) + byte_to_bit(file.read(1014))
                msg = str(fileSize).encode() + file.read(1014)
            else:
                #msg = byte_to_bit(file.read(1016))
                msg = file.read(1016)
            #Header
            comprimento = len(msg.encode())
            checksum = checksum_calculator(msg.encode())
            header_udp = struct.pack("!IIII", ORGN_PORT, DEST_PORT, comprimento, checksum)

            msg_headed = msg.encode() + header_udp
            udp.sendto(msg_headed, dest) # < o .encode() transforma a string em um arquivo em bits
            
            #num_pkt, serverADDR = udp.recvfrom(1024)
            #if(num_pkt != b'file end'):
            #    print("Pacote nº: ", num_pkt.decode())
            #    dados, serverADDR = udp.recvfrom(1024)
            #    dados = dados.decode().replace("\n", "")
            #    file.write(dados)
            #    print(dados)
            #else:
            #    fileEnd = True
        file.close()
    except(FileNotFoundError):
        print("[ARQUIVO NÃO EXISTE]")

print("\nCliente: Off\n")
udp.close()
