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

PROBAB_PERDA = 10 # um inteiro de 0 a 100
#   0 = Nunca vai perder pacote
# 100 = Sempre vai perder pacote

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orgn)

print("Cliente: On\nPara sair use CTRL+X\n")
print('Formato do nome: "nome"."tipo"\n\tExp.: nome_imagem.jpg\n')

while True:
    # SETUP: ------------------------------------------
    file_name = input("[Cliente]: ") # < qual o nome.tipo do arquivo pra ser enviado
    
    if(file_name == '\x18'):
        udp.sendto(file_name.encode(), dest)
        break

    udp.settimeout(2.0) 
    # ^ vai definir o tempo de esperar do temporizador
    # e fazer com que dê um erro de timeout quando passe dos 2seg
    # depois de entrar no modo de recebimento de pacotes
    try:
        file = open(f"cliente//{file_name}", "rb")
        fileSize = os.stat(f"cliente//{file_name}").st_size 
        # ^ quantidade de bytes do arquivo
    except(FileNotFoundError or PermissionError):
        print("[ARQUIVO NÃO EXISTE]")
        continue

    # ENVIAR O ARQUIVO: ------------------------------------------
    num_pkts = ceil(fileSize/1021) # < o número de pacotes em q o arquivo será enviado, sem contar com a inicial e o checksum
    # 1021 para o arquivo, 1 para o num de sequencia e 2 para o checksum
    count = -1 # < '-1' por causa do pacote inicial
    num_seq = b'\x00'
    
    sending = True
    while(sending):# [LOOP DE ENVIO]
        # WAIT SYSTEM CALL:
        #while(True):
            # como fazer para receber pacotes aqui para que sejam ignorados?
        #    above_call = input(f"Pkt type {num_seq}: ")
        #    if(above_call == num_seq):
        #        count += 1
        #        break
        
        # SEND PACKET:
        if(count == -1):
            msg = num_seq + (num_in_dec_num_bin_in_bin(num_pkts, "decimal") + file_name).encode()
            print('[Enviando pacote introdutório]')
        else:
            msg = num_seq + file.read(1021)
            print(f'[Enviando pacote {count+1}/{num_pkts}]')

        checksum = calc_checksum(msg)
        a = checksum+msg
        print(checksum+num_seq)
        if(not(gerador_perdas(PROBAB_PERDA))):
            udp.sendto(checksum+msg, dest)
            #          ^^^^^^^^^^^^ checksum[:16], num_seq[16:17], dados[17:]
        count += 1

        # WAIT ACK:
        ACK_rcvd = False
        while(not(ACK_rcvd)):
            try:
                dados, serverADDR = udp.recvfrom(1024)
                ACK_rcvd = isntCorrupt(dados) and isACK(dados, num_seq)
                print(f'[Recebido ACK {printACK(num_seq)}]')
            except(socket.timeout):
                print(f'[!!! Timer do ACK-{printACK(num_seq)} estourado !!!]')
                print(f'[Re-enviando pacote {count}/{num_pkts}]')
                if(not(gerador_perdas(PROBAB_PERDA))):
                    udp.sendto(checksum+msg, dest)

        # CHECK:
        num_seq = invertACK(num_seq)
        sending = count != num_pkts
    
    file.close()
    print('''_______________________________________
[ENVIO DE ARQUIVO: COMPLETO]
...
[AGUARDANDO RESPOSTA DO SERVIDOR...]
_______________________________________''')
    
    # RECEBER ARQUIVO E DUPLICAR: --------------------------------
    udp.setblocking(True)
    # ^ vai fazer o socket voltar a ficar esperando infinitamente
    # por um pacote no modo de recebimento, sem dar timeout
    
    count = 0
    num_seq = b'\x00'

    file_name = "copia_de_" + file_name
    copyFile = open(f"cliente//{file_name}", "wb")
    
    receiving = True
    while(receiving):# [LOOP DE RECEBIMENTO]
        packet, serverADDR = udp.recvfrom(1024)
        if(isACK(packet, num_seq) and isntCorrupt(packet)):
            count += 1
            print(f'[Recebido pacote {count}/{num_pkts}]')
            dados = packet[3:]
            copyFile.write(dados)
            print(f'[Enviando ACK {printACK(num_seq)}]')
            receiving = count != num_pkts # < pode ser q isso dê erro
        else:
            print(f'''.\n[Recebido pacote duplicado ou corrompido]
[Re-enviando ACK {printACK(num_seq)}]\n.''')
            num_seq = invertACK(num_seq) # tirar esse num_seq no futuro?
        checksum = calc_checksum(num_seq)
        if(not(gerador_perdas(PROBAB_PERDA))):
            udp.sendto(checksum+num_seq, dest)
        num_seq = invertACK(num_seq)

    copyFile.close()
    print(f'''_______________________________________
[RECEBIMENTO DE ARQUIVO: COMPLETO]
[CÓPIA DE ARQUIVO: COMPLETA]
_______________________________________''')

print("\nCliente: Off\n")
udp.close()
