import socket
import time # vai usar para dar os waits(talvez) e para pegar a hora atual

# Para começar a fazer os testes, precisa 1o criar um novo terminal,
# e depois precisa clicar naquele simbolozinho de duas janelas na aba do terminal
# depois escreve "py servidor\server.py" em um e "py client.py" no outro

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

msg = ''
while(msg != '\x18'):
    msg = input("[Cliente]: ") # < ação que o cliente deseja fazer
    udp.sendto(msg.encode(), dest) # < o .encode() transforma a string em um arquivo em bits
    fileEnd = False # < indicará quando o arquivo terminou para parar o loop de recebimento
    if(msg.capitalize() == "Chefia"):
        for i in range(2): 
            dados, serverADDR = udp.recvfrom(1024)
            print(f"[CINtofome]: {dados.decode()}")
            msg = input("[Cliente]: ")
            udp.sendto(msg.encode(), dest)
    
    while((msg == "1" or msg.capitalize() == "Cardárpio") and not(fileEnd)):
        num_pkt, serverADDR = udp.recvfrom(1024)
        if(num_pkt != b'file end'):
            print("Pacote nº: ", num_pkt.decode())
            dados, serverADDR = udp.recvfrom(1024)
            print(dados.decode())
        else:
            fileEnd = True

print("\nCliente: Off\n")
udp.close()
