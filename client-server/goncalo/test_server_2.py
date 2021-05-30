import pytest
import sys
import csv
import os
from server import * # importar todas as funções do servidor

gamers = {} # criar o dicionário global com a informação relativa aos clientes

# Função para testar
def test_end_to_end_1():
    client_sock = "socket1"
    client_id = "goncalo"

    # Começar jogo
    request = {'op': "START", 'client_id': client_id, 'cipher' : None} # dicionário de defeito, de pedido de começo de jogo ao servidor
    result = new_client(client_sock, request)
    if (result['status'] == True) :
        gamers.update(print_gamer()[client_id]) # atualizar o dicinário gamers local

    # Adivinha número
    request = {'op': "GUESS", 'number': number}
    result = guess_client(client_sock, request)


    #print(result) DEBUG
    #print(print_gamer()) DEBUG
    return result # contém o número secreto em print_gamer()

#def test_various_conditions():
    

# Testar a função de busca do id do cliente pelo socket
# Pré-requisitos: Registo no dicionário gamers
def test_find_client_id(client_sock) :
    return find_client_id(client_sock)

# Testar a funcionalidade de encritptação
# Pré-requisitos: Registo no dicionário gamers
def test_encription(client_id, number) :
    assert number == decrypt_intvalue(client_id, encrypt_intvalue(client_id, number))

# Testar a função new client do servidor SEM encriptação
# Pré-requisitos: nenhum
def test_new_client_non_encripted(client_sock, client_id) :
    request = {'op': "START", 'client_id': client_id, 'cipher' : None} # dicionário de defeito, de pedido de começo de jogo ao servidor
    result = new_client(client_sock, request)
    if (result['status'] == True) :
        gamers.update(print_gamer()[client_id]) # atualizar o dicinário gamers local
    #print(result) DEBUG
    #print(print_gamer()) DEBUG
    return result # contém o número secreto em print_gamer()

# Testar a função new client do servidor SEM encriptação
# Pré-requisitos: nenhum
def test_new_client_non_encripted_2(client_sock, client_id) :
    request = {'op': "START", 'client_id': client_id} # dicionário para pedir o começo de jogo ao servidor, sem o campo cipher
    result = new_client(client_sock, request)
    if (result['status'] == True) :
        gamers.update(print_gamer()[client_id]) # atualizar o dicinário gamers local
    #print(gamers) #DEBUG
    #print(print_gamer()) DEBUG
    return result

# Testar a função new client do servidor COM encriptação
# Pré-requisitos: nenhum
def test_new_client_encripted(client_sock, client_id, key) :
    chave = str (base64.b64encode (key), 'utf8') # guardar a chave (de modo codificado) no dicionário 
    request = {'op': "START", 'client_id': client_id, 'cipher' : chave} # dicionário de defeito, de pedido de começo de jogo ao servidor
    result = new_client(client_sock, request)
    #print(result) DEBUG
    #print(print_gamer()) DEBUG
    return result

# Testar a função de adivinhação do número secreto, SEM encriptação
# Pré-requisitos: o cliente existir, bem como o dicionário gamers
def test_guess_client_non_encripted(client_sock, number) :
    request = {'op': "GUESS", 'number': number}
    result = guess_client(client_sock, request)
    assert result['status'] == True, "ERRO!: Ocorreu um erro na operação GUESS" # garantir que não houve um erro
    return result

# Testar a função de adivinhação do número secreto, COM encriptação
# Pré-requisitos: o cliente existir, bem como o dicionário gamers
def test_guess_client_encripted(client_sock, number) :
    client_id = find_client_id(client_sock)
    assert client_id != None
    
    request = {'op': "GUESS", 'number': encrypt_intvalue(client_id, number)}
    result = guess_client(client_sock, request)
    assert result['status'] == True, "ERRO!: Ocorreu um erro na operação GUESS" # garantir que não houve um erro
    return result

# Testar a função para parar o programa, SEM encriptação
# Pré-requisitos: o cliente existir, bem como o dicionário gamers
def test_stop_non_encripted(client_sock, number, attempts) :
    client_id = find_client_id(client_sock)
    assert client_id != None

    request = {"op": "STOP", "number": number, "attempts": attempts}
    result = stop_client(client_sock, request)
    assert result['status'] == True, "ERRO!: Ocorreu um erro na operação STOP" # garantir que não houve um erro
    return result

# Testar a função para parar o programa, COM encriptação
# Pré-requisitos: o cliente existir, bem como o dicionário gamers
def test_stop_encripted(client_sock, number, attempts) :
    client_id = find_client_id(client_sock)
    assert client_id != None

    request = {"op": "STOP", "number": encrypt_intvalue(client_id, number), "attempts": encrypt_intvalue(client_id, attempts)}
    result = stop_client(client_sock, request)
    assert result['status'] == True, "ERRO!: Ocorreu um erro na operação STOP" # garantir que não houve um erro
    return result

# Testar a funcionalidade de o cliente desistir
# Pré-requisitos: o cliente e o dicionário gammers existirem
def test_quit(client_sock) :
    result = quit_client(client_sock, {"op": "QUIT"})
    assert result['status'] == True, "ERRO!: Ocorreu um erro na operação QUIT" # garantir que não houve um erro
    return result

# Verificar que os dados foram acrescentados ao ficheiro
def check_file(request):
    file = open('report.csv', 'r') # abrir o ficheiro para ler 
    csv_reader = csv.reader(file, delimiter=';', fieldnames=['client_id', 'secret_number', 'max_plays', 'current_plays', 'result']) # guardar o ficheiro como leitura csv
    for row in csv_reader: # percorrer o ficheiro
        if(row['client_id'] == request['client_id'] and row['secret_number'] == request['secret_number'] and row['max_plays'] == request['max_plays'] and row['current_plays'] == request['current_plays'] and row['result'] == request['result']) :
            return True # linha correta encontrada
    return False # valor por defeito

# Testar a função update file
# Pré-requisitos: nenhum
def test_update_file(client_id, request) :
    result = update_file(client_id, request) # Gravar o valor do request no ficheiro
    assert check_file(request) # garantir que os dados foram gravados

def test_create_file() :
    create_file()
    assert os.path.exists("report.csv"), "ERRO!: ficheiro não existe"

def main() :
    test_create_file()
    test_update_file("teste", {'client_id' : 'teste', 'secret_number': 12, 'max_plays' : 13, 'current_plays' : 6, 'result' : "Middle"}) # the values of request don't need to be real world valid tries
    
    test_create_file() # limpar os dados existentes no ficheiro
    test_new_client_non_encripted("socket1", "goncalo")
    assert test_new_client_non_encripted("socket2", "goncalo")['status'] == False, "Ocorreu um erro" # Este teste, tem de falhar
    test_new_client_non_encripted("socket2", "francisco")
    test_new_client_encripted("socket3", "manuel", key = os.urandom(16))

    

    test_create_file() # limpar os dados existentes no ficheiro
    # limpamos o ficheiro, pois é uma regra comum de no final de cada sessão de testes "deixar-mos" o sistema da mesma maneira que o encontrámos

if __name__ == "__main__":
	main()