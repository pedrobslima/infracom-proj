import socket
from funcoes import *

ORGN_HOST = "localhost"  # < endereço IP do servidor (127.0.0.1 é o padrão)
ORGN_PORT = 5000         # < porta do servidor
orgn = (ORGN_HOST, ORGN_PORT) # < vai servir para associar essa máquina ao cliente

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orgn)

print("Servidor: On\n")

dados = ''
# Assim que entrar no loop, o socket udp já é criado no
# modo blocking por default, então faz mais sentido 
# usar o .setblocking(True) no final do loop
while True:
    # SETUP: -----------------------------------------------------
    dados, clientADDR = udp.recvfrom(1024)
    if(dados == b'\x18'):
        break

    # RECEBER E ARMAZENAR: ---------------------------------------
    print('[Recebido pacote introdutório]')
    dados = dados.decode()
    num_pkts = bin_to_dec(dados[:16])
    file_name = dados[16:]

    recvFile = open(f"servidor//{file_name}", "wb")
    
    count = 0
    num_seq = '0'

    receiving = True
    while(receiving):# [LOOP DE RECEBIMENTO]
        # deveria adicionar condição para verificar 
        # se o endereço do cliente é o mesmo do pacote inicial?
        packet, clientADDR = udp.recvfrom(1024)
        if(isACK(packet, num_seq) and isntCorrupt(packet)):
            count += 1
            print(f'[Recebido pacote {count}/{num_pkts}]')
            dados = packet.split()[1] # < temporário, só para representar oq é pra fazer
            recvFile.write(dados)
            print(f'[Enviando ACK {num_seq}]')
            udp.sendto(num_seq.encode(), clientADDR)
            num_seq = invertACK(num_seq)
            receiving = count != num_pkts # < pode ser q isso dê erro
        else:
            print(f'''.\n[Recebido pacote duplicado ou corrompido]
[Re-enviando ACK {num_seq}]\n.''')
            udp.sendto(invertACK(num_seq).encode(), clientADDR)
    
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
    num_seq = '0'

    recvFile = open(f"servidor//{file_name}", "rb")
    sending = True
    while(sending):# [LOOP DE ENVIO]
        # WAIT SYSTEM CALL:
        while(True):
            # como fazer para receber pacotes aqui para que sejam ignorados?
            above_call = input(f"Pkt type {num_seq}: ")
            if(above_call == num_seq):
                count += 1
                break
            
        # SEND PACKET:
        msg = recvFile.read(1024)
        print(f'[Enviado pacote {count}/{num_pkts}]')
        #msg = '0'.encode() + data + checksum.encode()
        #^[1024] ^[- de 1]      ^[~1008]    ^[16]
        
        udp.sendto(msg, clientADDR)

        # WAIT ACK:
        ACK_rcvd = False
        while(not(ACK_rcvd)):
            try:
                dados, clientADDR = udp.recvfrom(1024)
                ACK_rcvd = isntCorrupt(dados) and isACK(dados, num_seq)
            except(socket.timeout):
                print(f'[!!! Timer do ACK-{num_seq} estourado !!!]')
                print(f'[Re-enviando pacote {count}/{num_pkts}]')
                udp.sendto(msg, clientADDR)

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