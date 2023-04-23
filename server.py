import socket
from funcoes import *

ORGN_HOST = "localhost"  # < endereço IP do servidor (127.0.0.1 é o padrão)
ORGN_PORT = 5000         # < porta do servidor
orgn = (ORGN_HOST, ORGN_PORT) # < vai servir para associar essa máquina ao cliente

PROBAB_PERDA = 10 # um inteiro de 0 a 100
#   0 = Nunca vai perder pacote
# 100 = Sempre vai perder pacote

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orgn)

print("Servidor: On\n")

dados = ''
# Assim que entrar no loop, o socket udp já é criado no
# modo blocking por default, então faz mais sentido 
# usar o .setblocking(True) no final do loop
while True:
    # SETUP: -----------------------------------------------------
    count = -1
    num_seq = b'\x00' # < deixar essa declaração inicial fora do loop?

    # RECEBER E ARMAZENAR: ---------------------------------------
    receiving = True
    while(receiving):# [LOOP DE RECEBIMENTO]
        # deveria adicionar condição para verificar 
        # se o endereço do cliente é o mesmo do pacote inicial?
        packet, clientADDR = udp.recvfrom(1024)
        if(isACK(packet, num_seq) and isntCorrupt(packet)):
            dados = packet[3:]
            count += 1
            if(count == 0):
                print('[Recebido pacote introdutório]')
                dados = dados.decode()
                print(dados)
                num_pkts = int(dados[0:16], 2)
                file_name = dados[16:]
                recvFile = open(f"servidor//{file_name}", "wb")
            else:
                print(f'[Recebido pacote {count}/{num_pkts}]')
                recvFile.write(dados)
                
            print(f'[Enviando ACK {printACK(num_seq)}]')    
            receiving = count != num_pkts # < pode ser q isso dê erro
        else:
            print(f'''.\n[Recebido pacote duplicado ou corrompido]
[Re-enviando ACK {printACK(num_seq)}]\n.''')
            num_seq = invertACK(num_seq) # tirar esse num_seq no futuro?
        checksum = calc_checksum(num_seq)
        if(not(gerador_perdas(PROBAB_PERDA))):
            udp.sendto(checksum+num_seq, clientADDR)
        num_seq = invertACK(num_seq)
    
    recvFile.close()
    print(f'''_______________________________________
[TRANSFERÊNCIA DE ARQUIVO: COMPLETA]
...
[INICIANDO ENVIO DO ARQUIVO...]
_______________________________________''')

    # ENVIAR DE VOLTA: -------------------------------------------
    udp.settimeout(2.0)
    # ^ vai definir o tempo de esperar do temporizador
    # e fazer com que dê um erro de timeout quando passe dos 2seg
    # depois de entrar no modo de recebimento de pacotes

    count = 0
    num_seq = b'\x00'

    recvFile = open(f"servidor//{file_name}", "rb")
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
        msg = num_seq + recvFile.read(1021)
        checksum = calc_checksum(msg)
        if(not(gerador_perdas(PROBAB_PERDA))):
            udp.sendto(checksum+msg, clientADDR)
        count += 1

        print(f'[Enviado pacote {count}/{num_pkts}]')
        #msg = '0'.encode() + data + checksum.encode()
        #^[1024] ^[- de 1]      ^[~1008]    ^[16]

        # WAIT ACK:
        ACK_rcvd = False
        while(not(ACK_rcvd)):
            try:
                dados, clientADDR = udp.recvfrom(1024)
                ACK_rcvd = isntCorrupt(dados) and isACK(dados, num_seq)
                print(f'[Recebido ACK {printACK(num_seq)}]')
            except(socket.timeout):
                print(f'[!!! Timer do ACK-{printACK(num_seq)} estourado !!!]')
                print(f'[Re-enviando pacote {count}/{num_pkts}]')
                if(not(gerador_perdas(PROBAB_PERDA))):
                    udp.sendto(checksum+msg, clientADDR)

        # CHECK:
        num_seq = invertACK(num_seq)
        sending = count != num_pkts
    
    recvFile.close()
    udp.setblocking(True)
    print('''_______________________________________
[ENVIO DE ARQUIVO: COMPLETO]
...
[AGUARDANDO RESPOSTA DO CLIENTE...]
_______________________________________''')

print("\nServidor: Off")
udp.close()