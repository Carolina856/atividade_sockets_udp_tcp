import socket
import operator

def calc_result(received_msg):
    operadores = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }

    #CALC:<n>:<operando1>:<op>:<operando2>
    msg = received_msg.split(":")
    print(msg)
    num1 = int(msg[1])
    op_string = msg[2]
    num2 = int(msg[3])

    if op_string in operadores:
        resultado = operadores[op_string](num1, num2)
        print(f"{resultado}") 
        return resultado
    else:
        print(f"ERROR:n:mensagem de erro")
        

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 6789))
s.listen(1)
print(f"Servidor rodando")

while True:
    conn, addr = s.accept()
    print(f"conectado por {addr}")

    data = conn.recv(1024)
    if data:
        msg = data.decode('utf-8')
        print(f"Mensagem recebida: {msg}")
        final_data = "RESULT:n:" + str(calc_result(msg))
        #print(f"RESULT:{n}:{resultado}")
        conn.sendall(bytes(final_data, 'utf-8'))

    conn.close()