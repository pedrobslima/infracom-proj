import socket
from math import ceil
import os
import time # vai usar para dar os waits(talvez) e para pegar a hora atual
import zlib # vai usar para o checksum
import struct# vai usar para o header em si do UDP 
from funcoes import *

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
DEST_PORT_BIN = num_in_dec_num_bin_in_bin(DEST_PORT, "dec")
ORGN_PORT_BIN = num_in_dec_num_bin_in_bin(ORGN_PORT, "dec")
#info = ORGN_HOST + ' ' + str(ORGN_PORT)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orgn)

print("Cliente: On\nPara sair use CTRL+X\n")

while(file_name != '\x18'):
    file_name = input("[Cliente]: ") # < qual o nome.tipo do arquivo pra ser enviado
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
        num_pkts = ceil((fileSize+2)/1016) # < o número de pacotes em q o arquivo será enviado, sem contar com a inicial
                                # ^ o +2 serão os dois bytes do primeiro pacote 
                                # que indicarão o tamanho total do arquivo
        for i in range(num_pkts+1):
            if(i == 0):
                msg = (num_in_dec_num_bin_in_bin(num_pkts, "decimal") + file_name).encode()
                #msg = num_in_dec_num_bin_in_bin(num_pkts, "decimal") + byte_to_bit(file.read(1014))
                #msg = str(fileSize).encode() + file.read(1014)
            else:
                msg = file.read(1016)
                msg_pro_checksum = byte_to_bit(msg)
            #Header
            #comprimento = 8 + len(msg) # < comprimento de bytes ou bits? Usei de bytes
                        # ^ 8 é o tamanho do header (sempre o msm)
            comprimento = num_in_dec_num_bin_in_bin((8 + len(msg)), "mede em bytes, mas precisa ser assim e em binario")
            # ^ mesma coisa do outro só que em bits
            #checksum = findChecksum(msg, k)
            checksum = '0000000000000000' # provisório
            #header_udp = struct.pack("!IIII", ORGN_PORT, DEST_PORT, comprimento, checksum)
            header_udp = ORGN_PORT_BIN + DEST_PORT_BIN + comprimento + checksum
            # ^ header é para ter 8 bytes (64 bits) 0000101110111000000100111000100000000000000101100000000000000000
            msg_headed = header_udp.encode() + msg
            #if(i == 1):
            #    print(len(header_udp))
            #    print(header_udp)
            #    print(msg_headed)
            #    teste = str(bit_to_byte(msg))

            #    print(teste[2:])
            #    tempo = input()
            udp.sendto(msg_headed, dest) # < o .encode() transforma a string em um arquivo em bits
        file.close()

        file_name = "copia_de_" + file_name
        copyFile = open(f"cliente//{file_name}", "wb")
        for i in range(num_pkts):
            data_bruto, serverADDR = udp.recvfrom(1024)
            header_udp, dados = unpack_msg(data_bruto)

            checksum = '0000000000000000' # provisório
            is_data_corrupted = checksum != header_udp[-16:] # pois assim podemos definitivamente comparar o checksum que entrou e saiu
            if(is_data_corrupted):
                print("Data Corruption status: " + is_data_corrupted) #aqui por motivos de teste
                break # ou sla faz qqr coisa

            dados = bit_to_byte(dados).decode() 
            # decode, encode, decode e encode por problemas de tipagem (str, bytes, bytearray e etc.)
            copyFile.write(dados.encode())

        copyFile.close()
    except(FileNotFoundError or PermissionError):
        print("[ARQUIVO NÃO EXISTE]")

print("\nCliente: Off\n")
udp.close()
