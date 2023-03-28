import socket

# Para começar a fazer os testes, precisa 1o criar um novo terminal,
# e depois precisa clicar naquele simbolozinho de duas janelas na aba do terminal
# depois escreve "py server.py" em um e "py client.py" no outro

HOST = "localhost"  # endereço IP do servidor (127.0.0.1 é o padrão)
PORT = 5000         # porta do servidor
dest = (HOST, PORT)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(("localhost", 3000))

print("Cliente: On\nPara sair use CTRL+X\n")

msg = ''
while(msg != '\x18'):
    msg = input()
    udp.sendto(msg.encode(), dest) # o .encode() transforma a string em um arquivo em bits
    if(msg == "1"):
        dados, serverADDR = udp.recvfrom(1024)
        print(dados.decode())
        #fileSize = int(dados.decode())
        #for i in range(fileSize):
        #    dados, serverADDR = udp.recvfrom(1024)
        #    print(dados.decode())

print("\nCliente: Off\n")
udp.close()
