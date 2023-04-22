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
    num_pkts = ceil(fileSize/1024) # < o número de pacotes em q o arquivo será enviado, sem contar com a inicial
    #num_pkts = ceil(fileSize/1008)
    count = -1 # < '-1' por causa do pacote inicial
    half_one_or_zero = '0' # nome temporário
    
    sending = True
    while(sending):# [LOOP DE ENVIO]
        # WAIT SYSTEM CALL:
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

        # WAIT ACK:
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
    
    # RECEBER ARQUIVO E DUPLICAR: --------------------------------
    udp.setblocking(True)
    # ^ vai fazer o socket voltar a ficar esperando infinitamente
    # por um pacote no modo de recebimento, sem dar timeout
    
    count = 0
    ACK: int # half_one_or_zero já vai representar o ACK, deixando aq só pra me lembrar

    file_name = "copia_de_" + file_name
    copyFile = open(f"cliente//{file_name}", "wb")
    
    receiving = True
    while(receiving):# [LOOP DE RECEBIMENTO]
        dadosBruto, serverADDR = udp.recvfrom(1024)
        #print(f'[Recebido pacote {count+1}/{num_pkts}]')
        if(count == 0):
            half_one_or_zero = dadosBruto.split()[0]
        if(isACK(dadosBruto, half_one_or_zero) and isntCorrupt(dadosBruto)):
            count += 1
            print(f'[Recebido pacote {count}/{num_pkts}]')
            dados = dadosBruto.split()[1] # < temporário, só para representar oq é pra fazer
            copyFile.write(dados)
            print(f'[Enviando ACK {half_one_or_zero}]')
            udp.sendto(half_one_or_zero.encode(), dest)
            half_one_or_zero = invertACK(half_one_or_zero)
            receiving = count != num_pkts # < pode ser q isso dê erro
        else:
            print(f'''.\n[Recebido pacote duplicado ou corrompido]
[Re-enviando ACK {half_one_or_zero}]\n.''')
            udp.sendto(invertACK(half_one_or_zero).encode(), dest)

    copyFile.close()
    print(f'''_______________________________________
[RECEBIMENTO DE ARQUIVO: COMPLETO]
[CÓPIA DE ARQUIVO: COMPLETA]
_______________________________________''')

print("\nCliente: Off\n")
udp.close()
