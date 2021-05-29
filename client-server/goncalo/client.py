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
    if "error" in response: #Se existir a chave error no dicionário enviado pelo server
        print(response['error']) #Mostra o erro
        return True 
    else: 
        return False


# process QUIT operation
def quit_action(client_sock, attempts):
    quit = {"op": "QUIT"} 
    recvquit = sendrecv_dict(client_sock, quit)
    if validate_response(client_sock, recvquit): return recvquit['error'] #se houver um erro dá return da chave do erro
    else:
        print(f"Desistiu do jogo depois de {attempts}") #Avisa o jogador que a operação foi efetuada
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
    tries = 0 # variavél usada para contar as tentativas feitas
    lastAttempt = 0 # variável usada para guardar a ultima tentativa do utilizador
    print("Bem vindo aoooooooooo Adivinha o número secreto!!!!")
    print("Deseja usar encriptação de dados?")
    answer = input("S/N? ").upper()
    while answer != "S" and answer != "N":
        answer = input("Inválido")
    start = {'op': "START", 'client_id': client_id, 'cipher' : None}
    key = None
    if answer == "S":
        key = os.urandom(16)
        key_tosend = str (base64.b64encode (key), 'utf8')
        start['cipher'] = key_tosend
        cipher = AES.new (key, AES.MODE_ECB)

    recvstart = sendrecv_dict(client_sock, start)
    if validate_response(client_sock, recvstart): return None
    print("Tentativas: " + str(recvstart['max_attempts']))
    
    while True:

        # Menu
        print("O que pretende fazer?")
        print("Adivinhar - 1")
        print("Terminar o jogo - 2")
        print("Desistir - 3")
        
        #Operação Guess
        try: 
            option = int(input(" "))
        except: option = 999 #Se for inserido algo que não seja um número
        if option == 1:
            while True :
                try : 
                    num = int(input("Adivinhe o número secreto: ")) # testar se o cliente introduziu um caracter ou número
                    break
                except :
                    print("Por favor introduza apenas números")
            if (key != None) :
                num = 
            guess = {'op': "GUESS", 'number': num}
            recvguess = sendrecv_dict(client_sock, guess)
            lastAttempt = num
            if validate_response(client_sock, recvguess): break
            tries += 1
            if recvguess['result'] == "equals":
                print("Acertaste")
                option = 2
            elif recvguess['result'] == "smaller":
                print("O número secreto é menor do que o inserido")
            elif recvguess['result'] == "larger":
                print("O número secreto é maior do que o inserido")
            else:
                print("FAILURE")

            if(tries >= recvstart['max_attempts']) : # deixa o jogador jogar n tentativas até m jogadas máximas, de forma a n = m
                print("Número máximo de tentativas obtido. O fim do jogo vai ser processado")
                option == 2
        #Operação Stop
        if option == 2:
            stop = {"op": "STOP", "number": lastAttempt, "attempts": tries}
            recvstop = sendrecv_dict(client_sock, stop) 
            if validate_response(client_sock, recvstop): break #Se for failure, é detetado como erro
            if((str(lastAttempt) == str(recvstop['guess']))) :
                print(f"As tuas tentativas deram fruto e conseguiste acertar, o número secreto era {recvstop['guess']} e conseguiste acertar com " + str(tries) + " tentativas")
            else : 
                print(f"O número secreto era {recvstop['guess']}! Pena que não conseguiste acertar, boa sorte para a próxima")
            exit(6) # Jogo completo
                
        #Operação Quit
        if option == 3:
            condition = quit_action(client_sock, tries)
            if condition == None: exit(7) #Se não houve erro
            else: #Se houver erro
                print(condition)
                exit(7)
        if(option < 1 or option > 3): print("Valor de operação inválido") #Se a opção inserida for inválida

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
    for i in range(0, len(argv[2]) - 1):
        if not argv[2][i].isdigit():
            print("Porta inválida! A porta só deve conter números")
            exit(3)

    if int(argv[2]) > 65535 or int(argv[2]) < 0:
        print("Porta inválida! Deve escrever um número entre 0 e 65535")
        exit(4)

    # Verifica a validade da máquina
    host = hostname.split('.')
    for i in range(0, len(host) - 1):
        if int(host[i]) < 0 or int(host[i]) > 255:
            print("Erro! A máquina é identificada da seguinte maneira:")
            print("X.X.X.X ,sendo X um número entre 0 e 255")
            exit(5)

    port = int(argv[2])

    # Socket
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Ligar ao servidor
    client_sock.connect((hostname, port))

    run_client(client_sock, argv[1])

    client_sock.close()
    exit(0)


if __name__ == "__main__":
    main(sys.argv)