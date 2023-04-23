def calc_checksum(data: bytes):
    # k: quant_bits de cada subdivisão da msg -> 
    #                         quant de subdivisões de 16bits da msg

    # SOMA
    soma = 0
    for i in range(len(data)):
        x = int.from_bytes(data[i:i+1], byteorder="big")
        soma += x
    soma = bin(soma)[2:]

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

    # EM BYTES
    checksum = (int(checksum, 2)).to_bytes(2, byteorder='big')
    print(checksum)
    return checksum

#def bin_to_dec(x: str): # LEMBRAR DE TROCAR ISSO
#    soma: int = 0
#    for i in range(16):
#        soma += (2**i) * int(x[-i-1])
#    return soma

# transforma o num decimal de bytes para um num binario de bits
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

def isntCorrupt(recvPkt: bytes):
    recv_checksum, data = recvPkt[:2], recvPkt[2:]
    checksum = calc_checksum(data)
    if(checksum != recv_checksum): print("Corrompido!")
    return checksum == recv_checksum

def isACK(recvPkt: bytes, ACK: bytes):
    print(ACK, recvPkt[2:3])
    if(ACK != recvPkt[2:3]): print("ACK ERRADO!")
    return ACK == recvPkt[2:3]

def invertACK(current: bytes):
    if(current == b'\x00'):
        return b'\x01'
    return b'\x00'

def printACK(num: bytes):
    temp = int.from_bytes(num, byteorder='big')
    return temp
