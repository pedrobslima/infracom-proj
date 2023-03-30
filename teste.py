import os
from math import ceil

def access_bit(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] >> shift) & 0x1

def byte_to_bit(x):
    y = ''
    for i in range(0, len(x)*8, 8):
        temp = ''
        for j in range(i, i+8):
            temp = str(access_bit(x, j)) + temp
        y = y + temp
    return y

send_msg = ''
fileSize = os.stat("servidor//cardapio.txt").st_size
print(f"Size: {fileSize} bytes")
# v definindo o número de pacotes que deverão ser enviados
num_pkts = ceil(fileSize/1016)
# v abrindo arquivo escolhido
#file = open("servidor\cardapio.txt", "rb") # < mudar o nome da variável para 'cardapio' msm?
file = open("servidor//cardapio.txt", "r")
for i in range(num_pkts): # loop para envio de pacotes
    #udp.sendto((str(i)).encode(), clientADDR) # < usado só para testes, diz qual o nº do pacote 
    data_bruto = map(bin,bytearray(file.read(1016).encode()))
    data_msg = "".join(data_bruto)
    #print(data_msg)
    send_msg = send_msg + data_msg
    #udp.sendto(send_msg, clientADDR)   
    # ^ ao usar o método .read(), a própria posição do cursor no arquivo 
    # mudará automaticamente para a posição pertencente ao 1025º byte
    # e assim segue, de 1024 bytes por 1024 bytes
    # Obs.: Se você pedir para o código ler uma quant de bytes 
    # maior do que resta, não vai dar erro nenhum
#udp.sendto('file end'.encode(), clientADDR)
# ^ é correto usar isso para sinalizar que o arquivo chegou ao seu fim?
file.close() # < fechando arquivo

file = open("servidor//cardapio.txt", "rb")
x = file.read(fileSize) 
y = ''
for i in range(0, len(x)*8, 8):
    temp = ''
    for j in range(i, i+8):
        temp = str(access_bit(x, j)) + temp
    y = y + temp
print(len(y) / len(x))
print(y)
#send_msg = send_msg.replace("b", "0")
print(send_msg)
print(y == send_msg)

file.close()