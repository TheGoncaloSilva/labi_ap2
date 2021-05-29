import pytest
import sys
import os
from server import * # importar todas as funções do servidor

gamers = {} # criar o dicionário global com a informação relativa aos clientes


def test_find_client_id(client_sock) :
    return find_client_id(client_sock)

def test_encription(client_id, number) :
    assert number == decrypt_intvalue(client_id, encrypt_intvalue(client_id, number))

def test_new_client_non_encripted(client_sock, client_id) : # testar a função new client do servidor
    request = {'op': "START", 'client_id': client_id, 'cipher' : None} # dicionário de defeito, de pedido de começo de jogo ao servidor
    result = new_client(client_sock, request)
    #print(result) DEBUG
    #print(print_gamer()) DEBUG
    return result # contém o número secreto em print_gamer()

def test_new_client_non_encripted_2(client_sock, client_id) : # testar a função new client do servidor
    request = {'op': "START", 'client_id': client_id} # dicionário para pedir o começo de jogo ao servidor, sem o campo cipher
    result = new_client(client_sock, request)
    #print(result) DEBUG
    #print(print_gamer()) DEBUG
    return result

def test_new_client_encripted(client_sock, client_id, key) : # testar a função new client do servidor
    chave = str (base64.b64encode (key), 'utf8') # guardar a chave (de modo codificado) no dicionário 
    request = {'op': "START", 'client_id': client_id, 'cipher' : chave} # dicionário de defeito, de pedido de começo de jogo ao servidor
    result = new_client(client_sock, request)
    #print(result) DEBUG
    #print(print_gamer()) DEBUG
    return result

def test_guess_client_non_encripted(client_sock, number) :
    request = {'op': "GUESS", 'number': number}
    result = guess_client(client_sock, request)
    return result

def test_guess_client_encripted(client_sock, number) :
    client_id = find_client_id(client_sock)
    assert client_id != None
    request = {'op': "GUESS", 'number': encrypt_intvalue(client_id, number)}
    result = guess_client(client_sock, request)
    assert result['status'] == True
    return result

def test_

def main(argv) : 
    test_new_client_non_encripted("teste1", "goncalo")
    test_new_client_non_encripted("teste2", "francisco")
    test_new_client_non_encripted("teste3", "manuel", key = os.urandom(16))

if __name__ == "__main__":
	main(sys.argv)