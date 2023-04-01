import zlib # vai usar para o checksum

def checksum_calculator(data):
    checksum = zlib.crc32(data)
    return checksum

def bit_to_byte(x):
    y = bytearray()
    for i in range(0, len(x), 8):
        byte = 0
        for j in range(i, i+8):
            byte = (byte << 1) | int(x[j])
        y.append(byte)
    return y

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

def bin_to_dec(x: str):
    soma: int = 0
    for i in range(16):
        soma += (2**i) * int(x[i])
    return soma

def unpack_msg(x: bytes):
    x = str(x.decode())
    return x[:64], x[64:] # < resto dos bytes de dados
        #  ^ 64bits do header     

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