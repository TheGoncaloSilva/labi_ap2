#!/usr/bin/python3

import sys
import socket
import select
import json
import base64
import csv
import random

from Crypto import Cipher
from common_comm import send_dict, recv_dict, sendrecv_dict

from Crypto.Cipher import AES

# Dicionário com a informação relativa aos clientes
# Exemplo do formato
# gammers = {
#			 ’manel’: { 'socket': <socket ... raddr=('127.0.0.1', 46196)>,
#						'cipher': b')6\x0c\xba\xf8\x14\xa7iU\xac\x8a~\xe0H~0',
#						'guess': 36, 'max_attempts': 22, 'attempts': 0 }
# }
gamers = {}

# return the client_id of a socket or None
def find_client_id (client_sock):
	for val in gamers:	# val tem o client_id de cada registo
		if client_sock.getpeername()[1] is gamers[val][0]['socket'].getpeername()[1]: # check address of each entry
   			return val # client_id found
	return None


# Função para encriptar valores a enviar em formato json com codificação base64
# return int data encrypted in a 16 bytes binary string and coded base64
def encrypt_intvalue (client_id, data):

	cipher = AES.new (gamers[client_id][0]['cipher'], AES.MODE_ECB) # Definir o algoritmo de encriptação tendo em conta a chave fornecida
	data = cipher.encrypt (bytes("%16d" % (data), 'utf8'))
	return str (base64.b64encode (data), 'utf8')
	


# Função para desencriptar valores recebidos em formato json com codificação base64
# return int data decrypted from a 16 bytes binary string and coded base64
def decrypt_intvalue (client_id, data):
	cipher = AES.new (gamers[client_id][0]['cipher'], AES.MODE_ECB) # Definir o algoritmo de encriptação tendo em conta a chave fornecida
	data = base64.b64decode (data)
	return cipher.decrypt (data)


#
# Incomming message structure:
# { op = "START", client_id, [cipher] }
# { op = "QUIT" }
# { op = "GUESS", number }
# { op = "STOP", number, attempts }
#
# Outcomming message structure:
# { op = "START", status, max_attempts }
# { op = "QUIT" , status }
# { op = "GUESS", status, result }
# { op = "STOP", status, guess }


#
# Suporte de descodificação da operação pretendida pelo cliente
#
def new_msg (client_sock):
	response = {}
	request = recv_dict (client_sock)
	#data = base64.b64decode (request['value'])
	#data = cipher.decrypt (data)
	op = request['op'].upper() # Operação escolhida pelo cliente (name.upper para não haver problemas com letras minúsculas e maiúsculas)
	cipher = request['cipher'] # cifra escolhida pelo utilizador
	if (op is 'START') :
		response = new_client(client_sock, request)
	elif (op is 'QUIT') :
		response = quit_client(client_sock, request)
	elif (op is 'GUESS') :
		response = guess_client(client_sock, request)
	elif (op is 'STOP') :
		response = stop_client(client_sock, request)
	else :
		response = { 'op': request['op'], 'status': False, 'error' : 'Operação Inválida' }

	#data = cipher.encrypt (bytes("%16d" % (data), 'utf8'))
	#data_tosend = str (base64.b64encode (data), 'utf8')
	result = send_dict (client_sock, response)
	return response
# read the client request
# detect the operation requested by the client
# execute the operation and obtain the response (consider also operations not available)
# send the response to the client


#
# Suporte da criação de um novo jogador - operação START
#
def new_client (client_sock, request):
	# obter o request e verificar guardar um novo registo no dicionário gamers
	# Check the return value and print message
	if (search_gamers(request['client_id']) != None):
  		return { 'op': 'START', 'status': False, 'error': 'Cliente existente' }

	secret_number = random.randint(0, 100) # Gera o número secreto
	max_Plays = random.randint(10, 30) # Gera o número máximo de tentativas

	gamers.update({request['client_id'] : [{ 'socket': client_sock, 'cipher' : request['cipher'],
			'guess' : secret_number, 'max_attempts' : max_Plays, 'attempts' : 0 }]})
	try :
		if(request['cipher'] != None) : # Se o cliente escolheu comunicar por encriptação
			max_Plays = encrypt_intvalue(request['client_id'], max_Plays) # encriptar o número de jogadas
	except : # se o campo cipher não existir, quer dizer que o utilizador não escolheu encriptar a ligação
		pass # continuar o program e enviar os dados como estavam

	return { 'op': 'START', 'status': 'True', 'max_attempts' : max_Plays }
# detect the client in the request
# verify the appropriate conditions for executing this operation
# obtain the secret number and number of attempts
# process the client in the dictionary
# return response message with results or error message

#
# Procurar no dicionário gamers
#
def search_gamers(value):
	for val in gamers:
		if value == gamers[val]: # Check each line 
   			return val # client_found


#
# Suporte da eliminação de um cliente
#
def clean_client (client_sock):
	return None
# obtain the client_id from his socket and delete from the dictionary


#
# Suporte do pedido de desistência de um cliente - operação QUIT
#
def quit_client (client_sock, request):
	client_id = find_client_id(client_sock) # Id do cliente devolvido pela função
	if (client_id == None):
  		return { 'op': 'QUIT', 'status': False, 'error': 'Cliente inexistente' }

	result = { 'client_id' : client_id, 'secret_number' : gamers[client_id][0]['guess'], 
	'max_plays' : gamers[client_id][0]['max_attempts'], 'current_plays' : gamers[client_id][0]['attempts'],
	'result' : 'QUIT'} # Dicionário para guardar no ficheiro json
	
	update_file(client_id, result)
	del gamers[client_id] # eliminar o cliente do dicionário de jogadores ativos
	return {'op': 'QUIT', 'status': True}
# obtain the client_id from his socket
# verify the appropriate conditions for executing this operation
# process the report file with the QUIT result
# eliminate client from dictionary
# return response message with result or error message


#
# Suporte da criação de um ficheiro csv com o respectivo cabeçalho
# <client_id> <secret_number> <max_attempts> <attempts_made> <result>
# result:
# 		QUIT -> cliente desiste
#		SUCCESS -> se o cliente acertou, respeitando o número máximo de jogadas
#		FAILURE -> se não acertou o nº secreto ou se excedeou o nº máximo de jogadas
#
def create_file ():
	# create report csv file with header
	file = open('report.csv', 'w') # abrir ou criar o ficheiro se não existir
	writer = csv.DictWriter(file, delimiter=',', fieldnames=['client_id', 'secret_number', 'max_plays', 'current_plays', 'result'])
	writer.writeheader() # Escrever os nomes das colunas

	file.close()
	return None

#
# Suporte da actualização de um ficheiro csv com a informação do cliente e resultado
#
def update_file (client_id, result):
	file = open('report.csv', 'w') # abrir o ficheiro
	writer = csv.DictWriter(file, delimiter=',', fieldnames=['client_id', 'secret_number', 'max_plays', 'current_plays', 'result'])
	writer.writerow(result)
	return None
# update report csv file with the result from the client


#
# Suporte da jogada de um cliente - operação GUESS
#
def guess_client (client_sock, request):
	client_id = find_client_id(client_sock) # Id do cliente devolvido pela função
	if (client_id == None):
  		return { 'op': 'GUESS', 'status': False, 'error': 'Cliente inexistente' }
	gamers[client_id][0]['attempts'] += 1 # contar uma tentativa
	result = ''
	if(request['number'] < gamers[client_id][0]['guess']) :
		result = 'larger'
	elif (request['number'] > gamers[client_id][0]['guess']) :
		result = 'smaller'
	else : 
		result = 'equals'

	return { 'op' : 'GUESS', 'status' : True, 'result' : result}
# obtain the client_id from his socket
# verify the appropriate conditions for executing this operation
# return response message with result or error message


#
# Suporte do pedido de terminação de um cliente - operação STOP
#
def stop_client (client_sock, request):
	client_id = find_client_id(client_sock) # Id do cliente devolvido pela função
	if (client_id == None):
  		return { 'op': 'STOP', 'status': False, 'error': 'Cliente inexistente' }

	response = {'op' : 'QUIT', 'status' : False, 'error' : 'Número de jogadas inconsistente/ Número secreto incorreto'}
	write = 'FAILURE'
	if (request['attempts'] is gamers[client_id][0]['attempts']) :
		if ((request['number'] is gamers[client_id][0]['guess']) and gamers[client_id][0]['attempts'] < gamers[client_id][0]['max_attempts']) :
			response = {'op' : 'STOP', 'status' : True, 'guess' : gamers[client_id][0]['guess']}
			write = 'SUCCESS'

	result = { 'client_id' : client_id, 'secret_number' : gamers[client_id][0]['guess'], 
	'max_plays' : gamers[client_id][0]['max_attempts'], 'current_plays' : gamers[client_id][0]['attempts'],
	'result' : write} # Dicionário para guardar no ficheiro json
			
	update_file(client_id, result)
	del gamers[client_id] # eliminar o cliente do dicionário de jogadores ativos

	return response

# obtain the client_id from his socket
# verify the appropriate conditions for executing this operation
# process the report file with the SUCCESS/FAILURE result
# eliminate client from dictionary
# return response message with result or error message


def main(argv):
	# validate the number of arguments and eventually print error message and exit with error
	# verify type of of arguments and eventually print error message and exit with error
	if(len(argv) <= 1) :
		print("Porto de acesso precisa de ser especificado")
		exit(1)
	if(int(argv[1]) <= 0) :
		print("Valor do porto tem de ser superior a 0")
		exit(2)
	
	port = int(argv[1])

	server_socket = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
	try:
		server_socket.bind (("127.0.0.1", port))
		server_socket.listen (10)
	except PermissionError:
		print("ERRO : Acesso negado com a porta de acesso fornecida")
		exit(1)
	except OSError:
		print("ERRO : O servidor já está a correr")
		exit(2)


	clients = []
	create_file ()

	while True:
		try:
			available = select.select ([server_socket] + clients, [], [])[0]
		except ValueError:
			# Sockets may have been closed, check for that
			for client_sock in clients:
				if client_sock.fileno () == -1: client_sock.remove (client) # closed
			continue # Reiterate select

		for client_sock in available:
			# New client?
			if client_sock is server_socket:
				newclient, addr = server_socket.accept ()
				clients.append (newclient)
			# Or an existing client
			else:
				# See if client sent a message
				if len (client_sock.recv (1, socket.MSG_PEEK)) != 0:
					# client socket has a message
					##print ("server" + str (client_sock))
					new_msg (client_sock)
				else: # Or just disconnected
					clients.remove (client_sock)
					clean_client (client_sock)
					client_sock.close ()
					break # Reiterate select

if __name__ == "__main__":
	main(sys.argv)
