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
    def __init__(self, udpSocket):
        self.name = "Stand By"

    def enter(self):
        pass

    def execute(self, inpt1, inpt2):
        if(inpt1.decode().capitalize() == "Chefia"):
            return True # testando

    def exit(self):
        #udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        pass

class WithClient(State):
    def __init__(self, udpSocket):
        self.name = "With Client"

    def enter(self):
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
        pass


class DuoStateMachine():
    def __init__(self, mySocket):
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
        self.currState(data, src)
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