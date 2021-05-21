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
def validate_response(client_sock, response):
    if "error" in response:
        print(response['error'])
    return None


# process QUIT operation
def quit_action(client_sock, attempts):
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
    while True:
        start = {'op': "START", 'id': client_id, [cipher]: cypherkey}
        recvstart = sendrecv_dict(client_sock, start)
        if "error" in recvstart:
            print(recvstart['error'])
            break

        # Menu
        print("O que pretende fazer?")
        print("Adivinhar - 1")
        print("Terminar o jogo - 2")
        print("Desistir - 3")

        option = int(input(" "))
        if option == 1:
            num = int(input("Adivinhe o número secreto:"))
            guess = {'op': "GUESS", 'number': num}
            recvguess = sendrecv_dict(client_sock, guess)
            tries += 1
            if "error" in recvguess:
                print(recvguess['error'])
                break
            if recvguess['result'] == "equals" and tries <= recvguess['max_attempts']:
                print("SUCESS")
            elif recvguess['result'] == "smaller":
                print("O número secreto é menor do que o inserido")
            elif recvguess['result'] == "bigger":
                print("O número secreto é maior do que o inserido")
            else:
                print("FAILURE")

        elif option == 2:
            stop = {"op": "STOP", "number": recvguess['number'], "attempts": tries}
            recvstop = sendrecv_dict(client_sock, stop)
            if "error" in recvstop:
                print(recvstop['error'])
            if stop[num] == recvstop[guess] and tries <= 30:
                print(f"O número era {recvstop[guess]}!")
                print("SUCESS")
            else:
                print
                

        elif option == 3:
            quit = {"op": "QUIT"}
            recvquit = sendrecv_dict(client_sock, quit)
            if "error" in recvquit:
                print(recvquit['error'])
            else:
                print("Desistiu do jogo")
            break

    return None


def main():
    # validate the number of arguments and eventually print error message and exit with error
    if len(sys.argv) != 4:
        print("Argumentos inválidos, deve ter o formato:")
        print("python3 client.py client_id porto [máquina]")
        sys.exit
    # verify type of of arguments and eventually print error message and exit with error

    # Verifica a validade do id do cliente
    if any(char.isdigit() for char in sys.argv[1]) or len(sys.argv[1]) <= 0:
        print("ID de client inválido!")
        sys.exit

    # Verifica a validade da porta
    for i in range(0, len(sys.argv[2]) - 1):
        if sys.argv[2][i].isalpha:
            print("Porta inválida! A porta não deve conter letras")
            sys.exit

    if sys.argv[2] > 65535 or sys.argv[2] < 0:
        print("Porta inválida! Deve escrever um número entre 0 e 65535")
        sys.exit

    # Verifica a validade da máquina
    host = sys.argv[3].split('.')
    for i in range(0, len(host) - 1):
        if host[i] < 0 or host[i] > 255:
            print("Erro! A máquina é identificada da seguinte maneira:")
            print("X.X.X.X ,sendo X um número entre 0 e 255")
            sys.exit

    # 127.0.0.1
    port = sys.argv[2]

    hostname = sys.argv[3]

    # Socket
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Ligar ao servidor
    client_sock.connect((hostname, port))

    run_client(client_sock, sys.argv[1])

    client_sock.close()
    sys.exit(0)


if __name__ == "__main__":
    main()
