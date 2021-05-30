#!/usr/bin/python3
# -*- coding: utf-8 -*-
# run program: python3 -m pytest test_client.py
import pytest
import os
import sys
import socket
import select
import json
import base64
import csv
import random
from Crypto import Cipher
from Crypto.Cipher import AES
from client import * # importar todas as funções do cliente

gamers = {} # criar o dicionário global com a informação relativa aos clientes

# Testar a função de busca do id do cliente pelo socket
# Pré-requisitos: Registo no dicionário gamers
def test_find_client_id() :
    write_gamer({'goncalo' : [{ 'socket': 'socket1', 'cipher' : None,
			'guess' : 12, 'max_attempts' : 24, 'attempts' : 0 }]}) # criar um resultado no servidor
    assert find_client_id("socket1") != None, "Cliente não encontrado" # garantir que o resultado ficou guardado
    clean_client('socket1') # apagar o resultado

# Testar a funcionalidade de encritptação
# Pré-requisitos: Registo no dicionário gamers
def test_encription() :
    key = os.urandom(16) # chave de encriptação
    write_gamer({'goncalo' : [{ 'socket': 'socket1', 'cipher' : key,
		'guess' : 12, 'max_attempts' : 24, 'attempts' : 0 }]}) # criar um resultado no servidor
    assert 29 == decrypt_intvalue('goncalo', encrypt_intvalue('goncalo', 29)) # garantir se o número fica o mesmo, depois de encriptar e desencriptar
    clean_client('socket1') # apagar o resultado

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
def test_update_file() :
    request = {'client_id' : 'teste', 'secret_number': 12, 'max_plays' : 13, 'current_plays' : 6, 'result' : "Middle"} # the values of request don't need to be real world valid tries
    update_file("teste", request) # Gravar o valor do request no ficheiro
    assert check_file(request) # garantir que os dados foram gravados

# Testar a função create file
# Pré-requisitos: nenhum
def test_create_file() :
    create_file()
    assert os.path.exists("report.csv"), "ERRO!: ficheiro não existe" # garantir que o ficheiro foi criado

def test_clean_client() :
    write_gamer({'ana' : [{ 'socket': 'socket10', 'cipher' : None,
		'guess' : 12, 'max_attempts' : 24, 'attempts' : 0 }]}) # criar um resultado no servidor
    assert clean_client('socket10'), "Cliente não existe"  # garantir que o resultado fica apagado

# Testar a função new client do servidor SEM encriptação
# Pré-requisitos: nenhum
def test_new_client_non_encripted() :
    request = {'op': "START", 'client_id': 'manel', 'cipher' : None} # dicionário de defeito, de pedido de começo de jogo ao servidor
    result = new_client('socket2', request) #criar o cliente
    assert result['status'], "Erro!: " + result['error']
    assert find_client_id('socket2') != None, "O cliente não existe" # garantir que o cliente existe
    #print(result) DEBUG
    #print(print_gamer()) DEBUG
    clean_client('socket2') # apagar o cliente

# Testar a função new client do servidor SEM encriptação
# Pré-requisitos: nenhum
def test_new_client_non_encripted_2() :
    request = {'op': "START", 'client_id': 'fernando'} # dicionário para pedir o começo de jogo ao servidor, sem o campo cipher
    result = new_client('socket3', request) # criar o cliente
    assert result['status'], "Erro!: " + result['error']
    assert find_client_id('socket3') != None, "O cliente não existe" # garantir que existe um cliente
    #print(gamers) #DEBUG
    #print(print_gamer()) DEBUG
    clean_client('socket3') # apagar o cliente

# Testar a função new client do servidor COM encriptação
# Pré-requisitos: nenhum
def test_new_client_encripted() :
    key = os.urandom(16) # gerar a chave
    chave = str (base64.b64encode (key), 'utf8') # guardar a chave (de modo codificado) no dicionário 
    request = {'op': "START", 'client_id': 'antonio', 'cipher' : chave} # dicionário de defeito, de pedido de começo de jogo ao servidor
    result = new_client('socket4', request) # criar o cliente
    assert result['status'], "Erro!: " + result['error']
    assert find_client_id('socket4') != None, "O cliente não existe" # garantir que o cliente existe
    #print(result) DEBUG
    #print(print_gamer()) DEBUG
    clean_client('socket4') # apagar o cliente

# Testar a função de adivinhação do número secreto, SEM encriptação
# Pré-requisitos: o cliente existir, bem como o dicionário gamers
def test_guess_client_non_encripted() :
    request = {'op': "START", 'client_id': 'goncalo1'} # dicionário para pedir o começo de jogo ao servidor, sem o campo cipher
    result = new_client('socket11', request) # criar o cliente
    assert result['status'], "Erro!: " + result['error']
    assert find_client_id('socket11') != None, "O cliente não existe" # garantir que existe um cliente

    request = {'op': "GUESS", 'number': 40} # criar o dicionário
    result = guess_client('socket11', request) # enviar o dicionário
    assert result['status'] == True, "ERRO!: Ocorreu um erro na operação GUESS" # garantir que não houve um erro
    clean_client('socket11')  # apagar o cliente

# Testar a função de adivinhação do número secreto, COM encriptação
# Pré-requisitos: o cliente existir, bem como o dicionário gamers
def test_guess_client_encripted() :
    key = os.urandom(16)
    chave = str (base64.b64encode (key), 'utf8') # guardar a chave (de modo codificado) no dicionário 
    request = {'op': "START", 'client_id': 'antonio1', 'cipher' : chave} # dicionário de defeito, de pedido de começo de jogo ao servidor
    result = new_client('socket12', request) # criar o cliente
    assert result['status'], "Erro!: " + result['error']
    assert find_client_id('socket12') != None, "O cliente não existe" # garantir que existe um cliente
    
    request = {'op': "GUESS", 'number': encrypt_intvalue('antonio1', 40)} # criar o dicionário
    result = guess_client('socket12', request) # enviar o dicionário
    assert result['status'] == True, "ERRO!: Ocorreu um erro na operação GUESS" # garantir que não houve um erro
    clean_client('12')  # apagar o cliente

# Testar a função para parar o programa, SEM encriptação
# Pré-requisitos: o cliente existir, bem como o dicionário gamers
def test_stop_non_encripted() :
    request = {'op': "START", 'client_id': 'felizmino'} # dicionário de defeito, de pedido de começo de jogo ao servidor
    result = new_client('socket5', request) # criar o cliente
    assert result['status'], "Erro!: " + result['error']
    assert find_client_id('socket5') != None, "O cliente não existe" # garantir que existe um cliente

    request = {"op": "STOP", "number": 25, "attempts": 1} # criar o dicionário
    result = stop_client('socket5', request) # enviar o dicionário
    assert result['status'] == True or result['op'] == 'QUIT', "ERRO!: Ocorreu um erro na operação STOP" # garantir que não houve um erro

# Testar a função para parar o programa, COM encriptação
# Pré-requisitos: o cliente existir, bem como o dicionário gamers
def test_stop_encripted() :
    key = os.urandom(16)
    chave = str (base64.b64encode (key), 'utf8') # guardar a chave (de modo codificado) no dicionário 
    request = {'op': "START", 'client_id': 'agostinho', 'cipher' : chave} # dicionário de defeito, de pedido de começo de jogo ao servidor
    result = new_client('socket6', request) # criar o cliente
    assert result['status'], "Erro!: " + result['error']
    assert find_client_id('socket6') != None, "O cliente não existe" # garantir que existe um cliente

    request = {"op": "STOP", "number": encrypt_intvalue('agostinho', 20), "attempts": encrypt_intvalue('agostinho', 1)} # criar o dicionário
    result = stop_client('socket6', request) # enviar o dicionário
    assert result['status'] == True or result['op'] == 'QUIT', "ERRO!: Ocorreu um erro na operação STOP" # garantir que não houve um erro

# Testar a funcionalidade de o cliente desistir
# Pré-requisitos: o cliente e o dicionário gamers existirem
def test_quit() :
    request = {'op': "START", 'client_id': 'agostinho'} # dicionário para pedir o começo de jogo ao servidor, sem o campo cipher
    result = new_client('socket6', request) # criar o cliente
    assert find_client_id('socket6') != None, "O cliente não existe" # garantir que existe um cliente
    assert result['status'], "Erro!: " + result['error']

    result = quit_client('socket6', {"op": "QUIT"}) # enviar a operação
    assert result['status'] == True, "ERRO!: Ocorreu um erro na operação QUIT" # garantir que não houve um erro

# Teste da criação de dois cliente com o mesmo identificador
# Pré-requisitos: nenhum
def test_new_client_fail(): 
    request = {'op': "START", 'client_id': 'mario', 'cipher' : None} # dicionário de defeito, de pedido de começo de jogo ao servidor
    result = new_client('socket2', request) #criar o cliente
    assert find_client_id('socket2') != None, "O cliente não existe" # garantir que o cliente existe
    assert result['status'], "Erro!: " + result['error']

    request = {'op': "START", 'client_id': 'mario', 'cipher' : None} # dicionário de defeito, de pedido de começo de jogo ao servidor
    result = new_client('socket3', request) #criar o cliente
    assert result['status'] == False, "Erro!: Verificação de clientes com o mesmo id não está a funcionar" # Tem de falhar

    clean_client('socket2') # apagar o cliente
    clean_client('socket3') # apagar o cliente

# Teste do acesso às funções com argumentos errados
def test_conditions() :
    assert new_client('socket20', {'op': "START", 'batatas' : 3})['status'] == False, "Erro!" # Testar se forem enviadas condições erradas para a função new_client (Tem de falhar)
    
    request = {'op': "START", 'client_id': 'maria', 'cipher' : None} # criar um novo cliente
    result = new_client('socket2', request) #criar o cliente
    assert find_client_id('socket2') != None, "O cliente não existe" # garantir que o cliente existe
    assert result['status'], "Erro!: " + result['error']
    assert guess_client('socket20', { 'op': 'GUESS', 'batatas' : 4})['status'] == False, "Erro!" # Testar se forem enviadas condições erradas para a função guess_client (Tem de falhar)

    # Testar se forem enviadas condições erradas para a função STOP_client
    assert stop_client('socket20', {'op': 'STOP', 'batatas' : 'estragadas'})['status'] == False, "Erro!" # Tem de falhar
    clean_client('socket20')# Função passada com sucesso