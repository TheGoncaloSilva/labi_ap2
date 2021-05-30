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

def test_validate_response() :
    response = {"op": 'GUESS', "client_id": 'manuel', "error": 'cliente inexistente'}
    response2 = {"op": 'GUESS', "client_id": 'manuel'}
    assert validate_response('socket1', response) == True, "ERRO! Não ocorreu validação"
    assert validate_response('socket2', response2) == False, "ERRO! Não ocorreu validação"

# Testar a funcionalidade de encritptação e desencriptação
def test_encription() :
    key = os.urandom(16) # chave de encriptação
    assert 29 == decrypt_intvalue(key, encrypt_intvalue(key, 29)) # garantir se o número fica o mesmo, depois de encriptar e desencriptar
    clean_client('socket1') # apagar o resultado

  