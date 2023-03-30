import os
from statemachine import State
import socket
file = open("servidor\cardapio.txt", "r")

x = os.stat("servidor\cardapio.txt").st_size

print(f"{x} bytes")

file.close()

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(("localhost", 5000))

class StandBy(State):
    def __init__(self, udpSocket: socket.socket):
        self.name = "Stand By"
        self.udpSocket = udpSocket # < isso causa algum tipo de problema?

    def enter(self):
        print("Servidor: Stand by") # < apenas pra teste, tirar dps
        pass

    def execute(self, inpt1, inpt2):
        if(inpt1.decode().capitalize() == "Chefia"):
            return True # testando

    def exit(self):
        pass
        #self.udpSocket.sendto('Digite seu ID')
        #cliente_id, clientADDR = self.udpSocket.recvfrom(1024)
        #self.udpSocket.sendto('Digite sua mesa')
        #cliente_mesa, clientADDR = self.udpSocket.recvfrom(1024)
        # Agoria teria a abertura do arquivo JSON 
        # e a adição do nova pessoa na mesa requisitada 
        # usando os dados que foram coletados

class WithClient(State):
    def __init__(self, udpSocket: socket.socket):
        self.name = "With Client"

    def enter(self):
        print("Servidor: On") # < apenas pra teste, tirar dps
        pass

    def execute(self, inpt1, inpt2):
        inpt1 = inpt1.decode()
        if(inpt1.capitalize() == "Cardapio" or inpt1 == "1"):
            #testar envio de arquivos por aqui
            pass
        if(inpt1.capitalize() == "Pedir" or inpt1 == "2"):
            pass
        elif(inpt1.capitalize() == "Conta individual" or inpt1 == "3"):
            pass
        elif(inpt1.capitalize() == "Conta da mesa" or inpt1 == "6"):
            pass
        elif(inpt1.capitalize() == "Passar"):
            pass
        elif(inpt1.capitalize() == "Levantar"):
            pass

    def exit(self):
        # Aqui teria a remoção do cliente da tabela de mesas,
        # mas como fazer isso? Preciso dos dados do cliente...
        pass


class DuoStateMachine():
    def __init__(self, mySocket: socket.socket):
        self.stateZero = StandBy(mySocket)
        self.stateOne = WithClient(mySocket)
        self.currState = self.stateZero
        self.nextState = self.stateOne
        # por mais que seja conveniente, não acho uma boa já abrir os 
        # arquivos aqui ou no início do código, corre risco de não 
        # fecharem por descuido nosso
    
    def transition(self):
        self.currState.exit()
        self.currState, self.nextState = self.nextState, self.currState
        self.currState.enter()

    def run(self, data, src):
        self.currState.execute(data, src) 
        # usar condicional aqui para já ordenar a transição de estado?
        # return cond = self.currState.execute(data, src)
        # if(cond): self.transition()?
        pass

# ========= PARA TESTES ===============
Server = DuoStateMachine(udp)
Server.transition()
print(Server.currState.name)

# =====================================
#class Server(StateMachine):
#    
#    # Estados
#    StandBy = State('estadoZero', initial = True)
#    WithClient = State('estadoUm')
#
#    # Transições

#class LightBulb(StateMachine):
# 
#    # creating states
#    offState = State("off", initial = True)
#    onState = State("on")
#      
#    # transitions of the state
#    switchOn = offState.to(onState)
#    switchOff = onState.to(offState)
#     
#         
#bulb = LightBulb()
#bulb.switchOn()
#print(bulb.current_state)