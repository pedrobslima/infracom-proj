import socket
from math import ceil
import os
import time # vai usar para dar os waits(talvez) e para pegar a hora atual
import zlib # vai usar para o checksum
import struct# vai usar para o header em si do UDP 
from funcoes import *

ORGN_HOST = "localhost"  # < endereço IP do servidor (127.0.0.1 é o padrão)
ORGN_PORT = 5000         # < porta do servidor
orgn = (ORGN_HOST, ORGN_PORT) # < vai servir para associar essa máquina ao cliente
ORGN_PORT_BIN = num_in_dec_num_bin_in_bin(ORGN_PORT, "dec")

#"C:\Users\pedro\Documents\NOVOdeltadelta\pog\infrasoft\infracom-proj\minosweep.jpg"
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orgn)
# Ainda tecnicamente precisa fazer os passos iniciais da criação
# da conexão via UDP, do cliente pedindo para criar uma conexão com o server
print("Servidor: On\n")

dados = ''
# Cada mensagem na vdd deverá ter 8128bits, ou seja, 1016 bytes
# por isso as partes retiradas do arquivo deverão ser de 1016 bytes
while True: # < adicionar parte de "Levantar da mesa" e da comida paga (ou talvez quando o número de cliente for 0?)
    data_bruto, clientADDR = udp.recvfrom(1024)
    #unpacking header
    header_udp, dados = unpack_msg(data_bruto)
    #header_udp = struct.unpack("!IIII", header_udp) #unpack é feito no header, é returnada uma tupla os 4 campos nós damos, então
    num_pkts = bin_to_dec(dados[:16])
    file_name = dados[16:] # < dps mudar para string

    checksum = '0000000000000000' # provisório
    if(checksum != header_udp[-16:]):
        continue # ignora o 2o loop se não bater os dois checksum
    
    DEST_HOST, DEST_PORT = clientADDR
    DEST_PORT_BIN = num_in_dec_num_bin_in_bin(DEST_PORT, "dec")

    recvFile = open(f"servidor//{file_name}", "wb")
    for i in range(num_pkts):
        data_bruto, clientADDR = udp.recvfrom(1024)
        header_udp, dados = unpack_msg(data_bruto)

        checksum = '0000000000000000' # provisório
        is_data_corrupted = checksum != header_udp[-16:] # pois assim podemos definitivamente comparar o checksum que entrou e saiu
        if(is_data_corrupted):
            print("Data Corruption status: " + is_data_corrupted) #aqui por motivos de teste
            break # ou sla faz qqr coisa

        recvFile.write(dados.encode())
    recvFile.close()

    recvFile.open(f"servidor//{file_name}", "rb")
    for i in range(num_pkts):
        msg = byte_to_bit(recvFile.read(1016))
        comprimento = num_in_dec_num_bin_in_bin((8 + (len(msg))/8), "mede em bytes, mas precisa ser assim e em binario")
        # ^ mesma coisa do outro só que em bits
        #checksum = findChecksum(msg, k)
        checksum = '0000000000000000' # provisório
        #header_udp = struct.pack("!IIII", ORGN_PORT, DEST_PORT, comprimento, checksum)
        header_udp = ORGN_PORT_BIN + DEST_PORT_BIN + comprimento + checksum
        # ^ header é para ter 8 bytes (64 bits) 0000101110111000000100111000100000000000000101100000000000000000
        msg_headed = header_udp + msg
        udp.sendto(msg_headed.encode(), clientADDR) # < o .encode() transforma a string em um arquivo em bits
    recvFile.close()
    