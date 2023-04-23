import random

def calc_checksum(data: bytes):
    # SOMA
    soma = 0
    for i in range(len(data)):
                # v transforma um byte em inteiro para fazer a soma
        x = int.from_bytes(data[i:i+1], byteorder="big") 
        soma += x
    soma = bin(soma)[2:]
            # ^ o [2:] é para tirar o '0b' que fica na esq da string dps do bin()

    # OVERFLOW
    if(len(soma) > 16):
        x = len(soma)-16
        soma = bin(int(soma[0:x], 2)+int(soma[x:], 2))[2:]
    if(len(soma) < 16):
        soma = soma.zfill(16)
 
    # COMPLEMENTO
    checksum = ''
    for i in soma:
        if(i == '1'):
            checksum += '0'
        else:
            checksum += '1'

    # EM BYTES (tem que ser assim, não adianta usar o .encode(), sério)
    checksum = (int(checksum, 2)).to_bytes(2, byteorder='big')

    return checksum

# transforma o num decimal de bytes para um num binario de bits,
# tem jeitos mais simples, mas n vale a pena perder tempo com isso
def num_in_dec_num_bin_in_bin(x: int, oq_x_mede: str): # < working title
    if(oq_x_mede == "bytes"):
        x *= 8 # < num de bits em decimal
    if(x > 65535):
        print("Conversão falhou")
    soma = str('')
    for i in range(15, -1, -1):
        div = 2**i
        if(x >= div):
            soma = soma + '1'
            x = x % div
        else:
            soma = soma + '0'
    return soma # num binario de 16bits

# diz se os dados se corromperam com o checksum
def isntCorrupt(recvPkt: bytes):
    recv_checksum, data = recvPkt[:2], recvPkt[2:]
    checksum = calc_checksum(data)
    if(checksum != recv_checksum): print("CORROMPIDO!")
    return checksum == recv_checksum

# verifica o ACK E O NÚMERO DE SEQUÊNCIA
def isACK(recvPkt: bytes, ACK: bytes):
    if(ACK != recvPkt[2:3]): print("ACK ERRADO!")
    return ACK == recvPkt[2:3]

# inverte o ACK E O NÚMERO DE SEQUÊNCIA
def invertACK(current: bytes):
    if(current == b'\x00'):
        return b'\x01'
    return b'\x00'

# print especial para o ACK E O NÚMERO DE SEQUÊNCIA
# (só para deixar os outros códigos mais ajeitados)
def printACK(num: bytes):
    temp = int.from_bytes(num, byteorder='big')
    return temp

# gerador de perdas
def gerador_perdas(probabilidade: int): # < como se fosse um d100 de rpg,
    roll = random.randint(0, 100)       # se o num aleatório gerado 
    if(roll < probabilidade):           # for menor que a probabilidade,
        print('PACOTE PERDIDO!')        # o pacote é dito como perdido
        return True
    return False