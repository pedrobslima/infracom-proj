import socket
from funcoes import *

ORGN_HOST = "localhost"  # < endereço IP do servidor (127.0.0.1 é o padrão)
ORGN_PORT = 5000         # < porta do servidor
orgn = (ORGN_HOST, ORGN_PORT) # < vai servir para associar essa máquina ao cliente

PROBAB_PERDA = 5 # um inteiro de 0 a 100 [podem mudar à vontade]
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
    num_seq = b'\x00' # < pfv não mudar para b'0' ou algo tipo

    # RECEBER E ARMAZENAR: ---------------------------------------
    receiving = True
    while(receiving):# [LOOP DE RECEBIMENTO]
        # deveria adicionar condição para verificar 
        # se o endereço do cliente é o mesmo do pacote inicial?
        packet, clientADDR = udp.recvfrom(1024)
        clientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientUDP.connect(clientADDR)
        if(isACK(packet, num_seq) and isntCorrupt(packet)):
            # PACOTE CERTINHO
            dados = packet[3:]
            count += 1
            if(count == 0):
                # PACOTE INTRODUTÓRIO
                print('[Recebido pacote introdutório]')
                dados = dados.decode()
                num_pkts = int(dados[0:16], 2)
                file_name = dados[16:]
                recvFile = open(f"servidor//{file_name}", "wb")
            else:
                # PACOTES DE CONTEÚDO DE ARQUIVO
                print(f'[Recebido pacote {count}/{num_pkts}]')
                recvFile.write(dados)
                
            print(f'[Enviando ACK {printACK(num_seq)}]')    
            receiving = count != num_pkts # < pode ser q isso dê erro
        else:
            # PACOTE COM ERRO
            print(f'''.\n[Recebido pacote duplicado ou corrompido]
[Re-enviando ACK {printACK(num_seq)}]\n.''')
            num_seq = invertACK(num_seq) # tirar esse num_seq no futuro?
        
        # FINAL DESSA REPETIÇÃO DO LOOP
        checksum = calc_checksum(num_seq) # calcula checksum
        if(not(gerador_perdas(PROBAB_PERDA))): # calcula se perdeu
            clientUDP.sendto(checksum+num_seq, clientADDR) # envia
        num_seq = invertACK(num_seq) # inverte num de sequência
    
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
    num_seq = b'\x00' # < pfv não mudar para b'0' ou algo tipo

    recvFile = open(f"servidor//{file_name}", "rb")
    sending = True
    while(sending):# [LOOP DE ENVIO]
        # SEND PACKET:
        msg = num_seq + recvFile.read(1021)
        checksum = calc_checksum(msg)
        if(not(gerador_perdas(PROBAB_PERDA))):
            udp.sendto(checksum+msg, clientADDR)
                      #^^^^^^^^^^^^ checksum[:2], num_seq[2:3], dados[3:]
        count += 1

        print(f'[Enviando pacote {count}/{num_pkts}]')

        # WAIT ACK:
        ACK_rcvd = False
        while(not(ACK_rcvd)): # < fica nesse estado até receber o ACK correto
            try:
                dados, clientADDR = udp.recvfrom(1024)
                # RECEBEU ACK
                ACK_rcvd = isntCorrupt(dados) and isACK(dados, num_seq) # < diz se é o ACK certo
                print(f'[Recebido ACK {printACK(num_seq)}]')
            except(socket.timeout):
                # TIMER ESTOROU
                print(f'[!!! Timer do ACK-{printACK(num_seq)} estourado !!!]')
                print(f'[Re-enviando pacote {count}/{num_pkts}]')
                if(not(gerador_perdas(PROBAB_PERDA))):
                    udp.sendto(checksum+msg, clientADDR)

        # CHECK DO LOOP:
        num_seq = invertACK(num_seq)
        sending = count != num_pkts
    
    recvFile.close()
    udp.setblocking(True)
    print('''_______________________________________
[ENVIO DE ARQUIVO: COMPLETO]
...
[AGUARDANDO RESPOSTA DO CLIENTE...]
_______________________________________''')

# Não tem mais como sair do loop normalmente, mas vou dxar assim msm
print("\nServidor: Off")
udp.close()