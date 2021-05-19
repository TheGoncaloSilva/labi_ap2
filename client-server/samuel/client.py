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
def encrypt_intvalue (cipherkey, data):
	return None


# Função para desencriptar valores recebidos em formato json com codificação base64
# return int data decrypted from a 16 bytes binary strings coded in base64
def decrypt_intvalue (cipherkey, data):
	return None


# verify if response from server is valid or is an error message and act accordingly
def validate_response (client_sock, response):
	return None


# process QUIT operation
def quit_action (client_sock, attempts):
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
def run_client (client_sock, client_id):
	return None
	

def main():
	# validate the number of arguments and eventually print error message and exit with error
	if len(sys.argv) != 4:
		print("Argumentos inválidos, deve ter o formato:")
		print("python3 client.py client_id porto [máquina]")
		sys.exit
	# verify type of of arguments and eventually print error message and exit with error
    
	#Verifica a validade do id do cliente
	if any(char.isdigit() for char in sys.argv[1]) or len(sys.argv[1]) <= 0:
		print("ID de client inválido!")
		sys.exit
    
	#Verifica a validade da porta
	for i in range(0, len(sys.argv[2]) - 1):
		if sys.argv[2][i].isalpha:
			print("Porta inválida! A porta não deve conter letras")
			sys.exit
    
	if sys.argv[2] > 65535 or sys.argv[2] < 0:
		print("Porta inválida! Deve escrever um número entre 0 e 65535")
		sys.exit
    
	#Verifica a validade da máquina
	host = sys.argv[3].split('.')
	for i in range(0, len(host) - 1):
         if host[i] < 0 or host[i] > 255:
            print("Erro! A máquina é identificada da seguinte maneira:")
			print("X.X.X.X ,sendo X um número entre 0 e 255")
			sys.exit

    #127.0.0.1
    port = sys.argv[2]

	hostname = sys.argv[3]
    
	#Socket
	client_sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

	#Ligar ao servidor
	client_sock.connect ((hostname, port))

	start = { "op": "START"}
	start["client_id"] = input("Nome: ")

	#
	if any(char.isdigit() for char in start["client_id"]) or len(start["client_id"]) <= 0:
		print("ID de client inválido!")
	else:
	    
        x = client_sock.sendrecv_dict(hostname, start)
	    if x = None:
	        print("Erro")
	  

	run_client (client_sock, sys.argv[1])

	client_sock.close ()
	sys.exit (0)

if __name__ == "__main__":
    main()
