def bin_to_dec(x: str):
    soma: int = 0
    for i in range(16):
        soma += (2**i) * int(x[-i-1])
    return soma

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

def isntCorrupt(recvPkt):
    _, data, recv_checksum = recvPkt.split() # < temporário, só para representar oq é pra fazer
    checksum: str
    #checksum = calculateChcksum(data)
    return checksum == recv_checksum

def isACK(recvPkt, ACK: str):
    recv_ACK = recvPkt.split()[0] # < temporário, só para representar oq é pra fazer
    return ACK == recv_ACK

def invertACK(current: str):
    if(current == '0'):
        return '1'
    return '0'

def calc_checksum(data): # < LEMBRAR DE FAZER ISSO DIREITO!!!
    return '0000000000000000'