import socket
from math import ceil
import os
from funcoes import *
#socket.setdefaulttimeout(2)
# Para começar a fazer os testes, precisa 1o criar um novo terminal,
# e depois precisa clicar naquele simbolozinho de duas janelas na aba do terminal
# depois escreve "py servidor\server.py" em um e "py client.py" no outro

y = '00000001'
x = b'1\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x03\x02\x02\x02\x02\x02\x03\x02\x02\x02\x03\x03\x03\x03\x04\x06\x04\x04\x04\x04\x04\x08\x06\x06\x05\x06\t\x08\n\n\t\x08\t\t\n\x0c\x0f\x0c\n\x0b\x0e\x0b\t\t\r\x11\r\x0e\x0f\x10\x10\x11\x10\n\x0c\x12\x13\x12\x10\x13\x0f\x10\x10\x10\xff\xdb\x00C\x01\x03\x03\x03\x04\x03\x04\x08\x04\x04\x08\x10\x0b\t\x0b\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\xff\xc2\x00\x11\x08\x07U\x05\x00\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1b\x00\x00\x02\x03\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\xff\xc4\x00\x1b\x01\x01\x01\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\xff\xda\x00\x0c\x03\x01\x00\x02\x10\x03\x10\x00\x00\x02\xe0{<\xe9X\xc4 Y\x16 \x00\x05\xd9\xb0\x96\x89V\x91@\x00!\xa4\xd1\x81"\xfb\x8a[\x8e:\x1c{\xdb\xe7\xf6]\xe7\xee\xbc\xfe\xca^\x8a\xaf]\x99J\xe4\xd6m\xbc\xf2k\xcfG~5\xfa\xb9\xc7\xd5\xe2\x9fN=\x8eW\xb9\xc7\xb7(\xe3\xef\xcd\x1d\xf1\xad\xb6\xd7\xa8\x99\xdb\xceqd\xe5u\x9d\x1a\xf5ra\xb8\xa7\xa62\xd72\xb1\xd8\t]\xc8\x08\xd9\x19\x15\xa9*\x1c\x8a\xc7N\xd8\xaa\x05p(\xb5\xad3X&\xb1K\x8f:\xab:Y\xd3\x81\x16\x12\xc8\x81cN\x8dI\x11\x80@9DE\x96l\x92\xf3ar\xc8\x19\xb5%nv\xe3P\x8b\x15\xc3Q\x83Qf\x95\x9f|:\xddx\xae\xf9&\xf9<\xfby\xee\x1d\x9f=-fY\xcf\xaf\xb8\xeb\xf4r\xbaZ\xee\xa4T\x84)PBP@\x14\x08B\x10\x00(l\xd7%\rA\x055\xb1\x00\x00\x0c\xd5\x10X\x08t\x00\x0eFI\x18\x13IMC\x8f\xafW\x97\xdd\xa3\xc9\xee\xa3\x97\xa8\xd6\x96t\xe6WL\xd3\xd3\x8d}\xbc\xd1\xed\xe6\xab~i\xfaxO\xb77d\xfar]3\xe9|w\x87\xe7\xeb\xd5\xd6\xf5\xeb<\x8d\xe3\x95+\xce\xfd\xe5x\xcc\xcfF\x9eW\xaec\xd1\xed\xe6<V\xf8\x9d&\xbe=z|\xee\xa4\xb0\xcfo:\xdc\x13\x9c7\x97\xa2F\x10\xd1\x05\xca\x1d\xa0)D\x01\t\x05\x8a\x84\xed\x8c\xb9\x9b\xcb7\x82k..~uf\x96\x998\x04\x01(\x16 \x87B]NL\xf1"\xc4\xd6^m&\xb3X\xd8\xc2T\xac\x01\x01\x19\xf7\xc7\xa5\xe8\xe1g|\x19\xdd\\\xba\xf8\xfcv\\v\xe4Gc\\\xfd>\xf1\x1d\xde{QhB\x10\t@\x10\x81@"$C\x12\x80m\xd7$\n@\x0b+$\xa2\x00\x19\xb1#,D\x01@\x00\xe4\x90\xd0\x18\xf1\xda\xdf\'\xbb\xa7\xe5\xf7\xe3\xf3\xfb/\xe7\xe8x\xd6~\x9c\x8e\xdc\xa5\xd3\x8e\x7fO\x96\x9fG\x91\xf5\xf3\xbe\xbcG$\x16\x17\'A\x9e\xbe\xdf\xc9\xbf\x0f9\x9d\xafS7\xd0\xf3\xcf\x97Xk~\xba<&\xb3\xb7y\xf4\xbd\'\x97=w~^G\xe9yV\xf3W\x93\xb3\xf3u\x87\x97O\x8e\xad\xba\xf5MU8\xdb\xb8\xb5\xd3\x04\xbc\xbd\xe2\xadEq\x1b\x96\x00\xcb\xa2\xc1T\xa4\xa0 4@\nZ\x96B\xcd\xa3\x17,\xde\x15\xcf5\x8f6\x19\xa4\xd1\x9af\x88\x02\x14\xc2\xac\xaa\xd1@J\x05J\x8bSA\xb2M\x84\xc2\xc6\n(\xa1\x16\'\xdf\x8e\xce\xfcJ\x8e:y\xbcv\xc1\xc3\xa0#S\x97\xb1\xdem\xdd\xe5\xdd&\x84!\x00(!\tX\x08\x88\x91\x12T 7k\x92\x05%P\x89\xec\xc6\x80A\x9b\x122\xc4A@\x00D\x91\xa0\xad\x16;t\xbc_N~/\xa4\xb8\xfat\xe7\xad=q\x0e\x9e,]<|\x0e\xfe\x7fA\xd7\x97\xbe\xeb\xc6\x1b\xe4\x8c\xbb\xb0g\x96d\xb8\xe6o#\xa6\xbe}{\xbc\xaf\x97\xe9\xc8\xe9\x93\x16x\x9d\xec\xebKXS\x85\xd6>\xb8\xeck\x1d\x0e]e\xdb\x1ew\xebx\xcfO\x18\xf1\xdc<\xfdW\xcf\xeb\x0f7Q\xaf^y\x9c\xe3.zC\x8f\xa7\xe8X\xba;\xf0\xab\xa6y{\xe7\x9f\\\xf9\xb6\xe4H\xdc\x96'

print(x[0:1].decode())
