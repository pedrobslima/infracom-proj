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

encerrado = False
msg = ''
while(msg != '\x18') and not encerrado:
    msg = input("[Cliente]: ") # < ação que o cliente deseja fazer
    udp.sendto(msg.encode(), dest) # < o .encode() transforma a string em um arquivo em bits
    fileEnd = False # < indicará quando o arquivo terminou para parar o loop de recebimento
    if(msg.capitalize() == "Chefia"):
        for i in range(3):
            dados, serverADDR = udp.recvfrom(1024)
            print(f"[CINtofome]: {dados.decode()}")
            msg = input("[Cliente]: ")
            udp.sendto(msg.encode(), dest)

    while((msg == "1" or msg.capitalize() == "Cardápio") and not(fileEnd)):
        tam_cardapio, serverADDR = udp.recvfrom(1024)
        print("[CINtofome]:")
        for i in range(int(tam_cardapio.decode())):
            item, serverADDR = udp.recvfrom(1024)
            print(item.decode())
        #num_pkt, serverADDR = udp.recvfrom(1024)
        # if(num_pkt != b'file end'):
        #     print("Pacote nº: ", num_pkt.decode())
        #     dados, serverADDR = udp.recvfrom(1024)
        #     print(dados.decode())
        # else:
        #     fileEnd = True

    if msg == '2' or msg.capitalize() == 'Pedido':
        dados, serverADDR = udp.recvfrom(1024)
        print(f"[CINtofome]: {dados.decode()}")
        msg = input("[Cliente]: ")
        udp.sendto(msg.encode(), dest)

    if msg == '3' or msg.capitalize() == 'Conta individual':
        dados, serverADDR = udp.recvfrom(1024)
        print(f"[CINtofome]: {dados.decode()}")

    if msg == '4' or msg.capitalize() == 'Conta da mesa':
        tam_mesa, serverADDR = udp.recvfrom(1024)
        for i in int(tam_mesa.decode()):
            contas, serverADDR = udp.recvfrom(1024)
            print(contas)
        msg = input("[Cliente]: ")
        udp.sendto(msg.encode(), dest)

    if msg == '5' or msg.capitalize() == 'Pagar':
        dados, serverADDR = udp.recvfrom(1024)
        msg = input("[Cliente]: ")
        udp.sendto(msg.encode(), dest)

    if msg == '6' or msg.capitalize() == 'Levantar':
        dados, serverADDR = udp.recvfrom(1024)
        print(f"[CINtofome]: {dados.decode()}")
        if dados.decode() == 'Voce ainda nao pagou sua conta':
            msg = input("[Cliente]: ")
            udp.sendto(msg.encode(), dest)
        else:
            encerrado = True

print("\nCliente: Off\n")
udp.close()
