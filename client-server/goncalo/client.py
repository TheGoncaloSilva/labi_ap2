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
	request = { 'op': 'START', client_id: 'cipher' }
	send_dict (client_sock, request)
	# print(request) Debug
	return None
	

def main(argv):
	# validate the number of arguments and eventually print error message and exit with error
	# verify type of of arguments and eventually print error message and exit with error
	assert len(argv) > 2, "Argumentos necessários tipo: <client_id> <porto> <máquina>"
	assert int(argv[1]) > 0, "Client_id tem de ser positivo"
	assert int(argv[2]) > 0, "Porto TCP do servidor tem de ser positivo"

	ip = "127.0.0.1"
	if(len(argv) == 4) :
		ip = argv[3]

	port = int(argv[2])
	hostname = ip

	client_sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	client_sock.bind ((ip, 0))
	try :
		client_sock.connect ((hostname, port))
	except PermissionError:
		print("ERRO : Acesso negado ao conectar com o servidor")
		exit(1)
	except OSError:
		print("ERRO : Não foi possível encontrar o servidor")
		exit(2)

	run_client (client_sock, sys.argv[1])

	client_sock.close ()
	sys.exit (0)

if __name__ == "__main__":
    main(sys.argv)
