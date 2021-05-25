#!/usr/bin/python3

import os
import sys
import socket
import json
import base64
from common_comm import send_dict, recv_dict, sendrecv_dict

from Crypto.Cipher import AES

# Função para encriptar valores a enviar em formato jsos com codificação base64
# return int data encrypted in a 16 bytes binary string coded in base64


def encrypt_intvalue(cipherkey, data):
    return None


# Função para desencriptar valores recebidos em formato json com codificação base64
# return int data decrypted from a 16 bytes binary strings coded in base64
def decrypt_intvalue(cipherkey, data):
    return None


# verify if response from server is valid or is an error message and act accordingly
# If true there's an error
def validate_response(client_sock, response):
    if "error" in response:
        print(response['error'])
        return True
    else: 
        return False


# process QUIT operation
def quit_action(client_sock, attempts):
    quit = {"op": "QUIT"}
    recvquit = sendrecv_dict(client_sock, quit)
    if validate_response: return recvquit['error']
    else:
        print(f"Desistiu do jogo depois de {attempts}")
        return None


# Outcomming message structure:
# { op = "START", client_id, [cipher] }
# { op = "QUIT" }
# { op = "GUESS", number }
# { op = "STOP", number, attempts }
#
# Incomming message structure:
# { op = "START", status, max_attempts }
# { op = "QUIT" , status }
# { op = "GUESS", status, result }
# { op = "STOP", status, guess }


#
# Suporte da execução do cliente
#
def run_client(client_sock, client_id):
    tries = 0
    print("Bem vindo aoooooooooo Adivinha o número secreto!!!!")
    print("Deseja usar encriptação de dados?")
    answer = input("S/N?")
    while not(input == "S" or input == "N"):
        answer = input("Inválido")
    start = {'op': "START", 'id': client_id, 'cipher' : None}
    if answer == "S":
        key = os.urandom(16)
        key_tosend = str (base64.b64encode (key), 'utf8')
        start['cypher'] = key_tosend
    recvstart = sendrecv_dict(client_sock, start)
    if validate_response(client_sock, recvstart): return None

    while True:

        # Menu
        print("O que pretende fazer?")
        print("Adivinhar - 1")
        print("Terminar o jogo - 2")
        print("Desistir - 3")
        
        #Operação Guess
        option = int(input(" "))
        if option == 1:
            num = int(input("Adivinhe o número secreto:"))
            guess = {'op': "GUESS", 'number': num}
            recvguess = sendrecv_dict(client_sock, guess)
            tries += 1
            if validate_response: break
            if recvguess['result'] == "equals" and tries <= recvstart['max_attempts']:
                print("SUCESS")
            elif recvguess['result'] == "smaller":
                print("O número secreto é menor do que o inserido")
            elif recvguess['result'] == "bigger":
                print("O número secreto é maior do que o inserido")
            else:
                print("FAILURE")
        
        #Operação Stop
        elif option == 2:
            stop = {"op": "STOP", "number": recvguess['number'], "attempts": tries}
            recvstop = sendrecv_dict(client_sock, stop)
            if validate_response: break
            if stop['number'] == recvstop['guess'] and tries <= recvstart['max_attempts']:
                print(f"O número era {recvstop[guess]}!")
                print("SUCESS")
            else:
                 print(f"O número era {recvstop[guess]}!")
                 print("SUCESS")
                
        #Operação Quit
        elif option == 3:
            quit_action(client_sock, tries)

    return None


def main(argv):
    # validate the number of arguments and eventually print error message and exit with error
    if len(argv) < 3 or len(argv) > 4:
        print("Argumentos inválidos, deve ter o formato:")
        print("python3 client.py client_id porto [máquina]")
        exit(1)
    elif len(argv) == 3:
        hostname = "127.0.0.1"
    else:
        hostname = argv[3]
    # verify type of of arguments and eventually print error message and exit with error

    # Verifica a validade do id do cliente
    if not len(argv[2]): 
        print("ID de client inválido!")
        exit(2)

    # Verifica a validade da porta
    for i in range(0, len(int(argv[2])) - 1):
        if not argv[2][i].isdigit():
            print("Porta inválida! A porta só deve conter números")
            exit(3)

    if int(argv[2]) > 65535 or int(argv[2]) < 0:
        print("Porta inválida! Deve escrever um número entre 0 e 65535")
        exit(4)

    # Verifica a validade da máquina
    host = argv[3].split('.')
    for i in range(0, len(host) - 1):
        if int(host[i]) < 0 or int(host[i]) > 255:
            print("Erro! A máquina é identificada da seguinte maneira:")
            print("X.X.X.X ,sendo X um número entre 0 e 255")
            exit(5)

    # 127.0.0.1
    port = argv[2]

    # Socket
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Ligar ao servidor
    client_sock.connect((hostname, port))

    run_client(client_sock, argv[1])

    client_sock.close()
    exit(0)


if __name__ == "__main__":
    main(sys.argv)