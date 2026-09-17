import socket
import operator
import random
import argparse

def calc_result(received_msg):
    operadores = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }

    msg = received_msg.split(":")
    num1 = int(msg[2])
    op_string = msg[3]
    num2 = int(msg[4])

    if op_string in operadores:
        try:
            result = operadores[op_string](num1, num2) 
            return "RESULT:" + msg[1] + ":" + str(result)
        except ZeroDivisionError:
            return "ERROR:" + msg[1] + ":Divisão por zero"
    else:
        return "ERROR:" + msg[1] + ":Aconteceu um erro"

#Configura os argumentos da linha de comando
parser = argparse.ArgumentParser(description="Servidor com perda simulada de datagramas.")
parser.add_argument(
    "--loss-rate",
    type = float,
    default = 0.1,
    help = "Fração de datagramas a serem descartadas (ex: 0.1 para 10 por cento)"
)
args = parser.parse_args()

LOSS_RATE = args.loss_rate
print(f"Servidor iniciado com taxa de perda de {LOSS_RATE * 100}%") 

HOST = ''
PORT = 6789
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
n = 0 #Número da mensagem recebida

while True:
    print(f"Esperando Msg {n} ...")
    data, address = s.recvfrom(1024)
    ip, porta = address
    msg = data.decode('utf-8')
    print(f"Cliente: {ip} - Porta: {porta}\nMsg: {msg}")

    #Calcula a perda simulada
    if random.random() <= LOSS_RATE: 
        #TRATAR CASO EM QUE O USUÁRIO INSERE LOSS_RATE > 1
        print(f"Msg {n} de {ip}:{porta} foi descartada")
        n += 1
        continue

    #Se o datagrama não foi perdido
    final_data = str(calc_result(msg))
    s.sendto(bytes(final_data, 'utf-8'), (ip, porta))
    n += 1