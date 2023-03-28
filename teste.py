import os
file = open("servidor\cardapio.txt", "r")

x = os.stat("servidor\cardapio.txt").st_size

print(f"{x} bytes")

file.close()
