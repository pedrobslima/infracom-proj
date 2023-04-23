import socket
from funcoes import *

ORGN_HOST = "localhost"  # < endereço IP do servidor (127.0.0.1 é o padrão)
ORGN_PORT = 5000         # < porta do servidor
orgn = (ORGN_HOST, ORGN_PORT) # < vai servir para associar essa máquina ao cliente

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orgn)

print("Servidor: On\n")

dados = ''
while True:
    # RECEBER E ARMAZENAR:
    dados, clientADDR = udp.recvfrom(1024)
    if(dados == b'\x18'):
        break
    print('[Recebido pacote introdutório]')
    dados = dados.decode()
    num_pkts = bin_to_dec(dados[:16])
    file_name = dados[16:]

    recvFile = open(f"servidor//{file_name}", "wb")
    for i in range(num_pkts):
        dados, clientADDR = udp.recvfrom(1024)
        print(f'[Recebido pacote {i+1}/{num_pkts}]')
        recvFile.write(dados)
    recvFile.close()

    # ENVIAR DE VOLTA
    print(f'''_______________________________________
[TRANSFERÊNCIA DE ARQUIVO: COMPLETA]
...
[INICIANDO ENVIO DO ARQUIVO...]
_______________________________________''')
    recvFile = open(f"servidor//{file_name}", "rb")
    for i in range(num_pkts):
        msg = recvFile.read(1024)
        print(f'[Enviando pacote {i+1}/{num_pkts}]')

        udp.sendto(msg, clientADDR) 
    recvFile.close()
    print('''_______________________________________
[ENVIO DE ARQUIVO: COMPLETO]
...
[AGUARDANDO RESPOSTA DO CLIENTE...]
_______________________________________''')

print("\nServidor: Off")
udp.close()