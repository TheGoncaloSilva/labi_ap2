
import pytest
import sys
import csv
import os
from server import * # importar todas as funções do servidor

gamers = {} # criar o dicionário global com a informação relativa aos clientes

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
    #print(result) DEBUG
    #print(print_gamer()) DEBUG
    return result # contém o número secreto em print_gamer()

# Testar a função new client do servidor SEM encriptação
# Pré-requisitos: nenhum
def test_new_client_non_encripted_2(client_sock, client_id) :
    request = {'op': "START", 'client_id': client_id} # dicionário para pedir o começo de jogo ao servidor, sem o campo cipher
    result = new_client(client_sock, request)
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
    assert result['status'] == True or result['op'] == 'QUIT', "ERRO!: Ocorreu um erro na operação STOP" # garantir que não houve um erro
    return result

# Testar a função para parar o programa, COM encriptação
# Pré-requisitos: o cliente existir, bem como o dicionário gamers
def test_stop_encripted(client_sock, number, attempts) :
    client_id = find_client_id(client_sock)
    assert client_id != None

    request = {"op": "STOP", "number": encrypt_intvalue(client_id, number), "attempts": encrypt_intvalue(client_id, attempts)}
    result = stop_client(client_sock, request)
    assert result['status'] == True or result['op'] == 'QUIT', "ERRO!: Ocorreu um erro na operação STOP" # garantir que não houve um erro
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
    csv_reader = csv.reader(file, delimiter=';') # guardar o ficheiro como leitura csv
    for row in csv_reader: # percorrer o ficheiro
        if(str(row[0]) == str(request['client_id']) and int(row[1]) == int(request['secret_number']) and int(row[2]) == int(request['max_plays']) and int(row[3]) == int(request['current_plays']) and str(row[4]) == str(request['result'])) :
            return True # linha correta encontrada
    return False # valor por defeito

# Testar a função update file
# Pré-requisitos: ficheiro criado
def test_update_file(client_id, request) :
    result = update_file(client_id, request) # Gravar o valor do request no ficheiro
    assert check_file(request) # garantir que os dados foram gravados

# Testar a função create file
# Pré-requisitos: nenhum
def test_create_file() :
    create_file()
    assert os.path.exists("report.csv"), "ERRO!: ficheiro não existe" # garantir que o ficheiro foi criado

def test_clean_client() :
    print("todo")

def main() :
    test_create_file()
    test_update_file("teste", {'client_id' : 'teste', 'secret_number': 12, 'max_plays' : 13, 'current_plays' : 6, 'result' : "Middle"}) # the values of request don't need to be real world valid tries
    
    # Test Case 1.1, exceed number os tries and dont get the number right
    test_create_file() # limpar os dados existentes no ficheiro
    test_new_client_non_encripted("socket1", "goncalo")
    assert test_find_client_id("socket1") != None # garantir que o cliente foi criado
    assert test_new_client_non_encripted("socket2", "goncalo")['status'] == False, "Ocorreu um erro" # Este teste, tem de falhar
    # print(print_client("goncalo")) DEBUG
    attempts = print_client("goncalo")[0]['attempts']
    max_attempts = print_client("goncalo")[0]['max_attempts']
    while attempts <= max_attempts + 1 :
        if(print_client("goncalo")[0]['guess'] > 50) :
            test_guess_client_non_encripted("socket1", 40)
            number = 40
        else :
            test_guess_client_non_encripted("socket1", 60)
            number = 60
        attempts += 1
    test_stop_non_encripted("socket1", number, attempts)

    # Test Case 1.2, exceed number os tries and dont get the number right with encription
    test_new_client_encripted("socket2", "francisco", key = os.urandom(16))
    assert test_find_client_id("socket2") != None # garantir que o cliente foi criado
    # print(print_client("francisco")) DEBUG
    attempts = print_client("francisco")[0]['attempts']
    max_attempts = print_client("francisco")[0]['max_attempts']
    while attempts <= max_attempts + 1 :
        if(print_client("francisco")[0]['guess'] > 50) :
            test_guess_client_encripted("socket2", 40)
            number = 40
        else :
            test_guess_client_encripted("socket2", 60)
            number = 60
        attempts += 1
    test_stop_encripted("socket2", number, attempts)


    test_new_client_encripted("socket3", "manuel", key = os.urandom(16))
    assert test_find_client_id("socket3") != None # garantir que o cliente foi criado

    

    test_create_file() # limpar os dados existentes no ficheiro
    # limpamos o ficheiro, pois é uma regra comum de no final de cada sessão de testes "deixar-mos" o sistema da mesma maneira que o encontrámos

if __name__ == "__main__":
	main()