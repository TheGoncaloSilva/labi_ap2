#encode = 'utf-8'
#run program: python3 -m pytest test_func.py
import pytest
import random
import time
from subprocess import Popen
from subprocess import PIPE

#Popen ("killall python3", stdout = PIPE, shell=True) # Acabar com processos de python que estejam a correr

# Testar o servidor sem argumentos de entrada
def test_no_condition_server ():
    cmd = Popen ("python3 server.py", stdout = PIPE, shell=True)
    assert cmd.wait() == 4 #Check Return Code
    assert cmd.stdout.read ().decode ('utf-8') == "Porto de acesso precisa de ser especificado\n"

# Testar o servidor com letras em vez de números no campo do porto nos argumentos de entrada
def test_bad_condition_server ():
    cmd = Popen ("python3 server.py batatas", stdout = PIPE, shell=True)
    assert cmd.wait() == 4 #Check Return Code
    assert cmd.stdout.read ().decode ('utf-8') == "O valor do porto de acesso precisa de ser um número\n"

# Testar o servidor com um número de porta errado
def test_bad_condition_server_2 ():
    cmd = Popen ("python3 server.py 100000000", stdout = PIPE, shell=True)
    assert cmd.wait() == 4 #Check Return Code
    assert cmd.stdout.read ().decode ('utf-8') == "Valor do porto tem de ser superior a 0 e inferior a 65535\n"

    cmd = Popen ("python3 server.py -1", stdout = PIPE, shell=True)
    assert cmd.wait() == 4 #Check Return Code
    assert cmd.stdout.read ().decode ('utf-8') == "Valor do porto tem de ser superior a 0 e inferior a 65535\n"

# Testar o cliente com argumentos de entrada errados
def test_no_condition_client ():
    # Testar o cliente sem argumentos de entrada
    cmd = Popen ("python3 client.py", stdout = PIPE, shell=True)
    assert cmd.wait() == 4 #Check Return Code
    assert cmd.stdout.read ().decode ('utf-8') == "ERRO!: Argumentos inválidos, deve ter o formato:\npython3 client.py client_id porto [máquina]\n"
    
    # Testar o cliente com argumentos de entrada incompletos
    cmd = Popen ("python3 client.py testeId", stdout = PIPE, shell=True)
    assert cmd.wait() == 4 #Check Return Code
    assert cmd.stdout.read ().decode ('utf-8') == "ERRO!: Argumentos inválidos, deve ter o formato:\npython3 client.py client_id porto [máquina]\n"

# Testar o cliente com argumentos de entrada errados
def test_condition () :
    # Campo porto com letras invés de números
    cmd = Popen ("python3 client.py testeId batatas", stdout = PIPE, shell=True)
    assert cmd.wait() == 4 #Check Return Code
    assert cmd.stdout.read ().decode ('utf-8') == "ERRO!: Porta inválida! A porta só deve conter números\n"

    # Campo porto com valor impossível
    cmd = Popen ("python3 client.py testeId 1000000", stdout = PIPE, shell=True)
    assert cmd.wait() == 4 #Check Return Code
    assert cmd.stdout.read ().decode ('utf-8') == "ERRO!: Porta inválida! Deve escrever um número entre 0 e 65535\n"

    # Campo máquina com letras invés de números
    cmd = Popen ("python3 client.py testeId 1234 127.batatas.0.1", stdout = PIPE, shell=True)
    assert cmd.wait() == 4 #Check Return Code
    assert cmd.stdout.read().decode('utf-8') == "ERRO!: A máquina tem de ter números inteiros:\n"
    
    # Campo máquina com valores irrealistas
    cmd = Popen ("python3 client.py testeId 1234 127.300.0.1", stdout = PIPE, shell=True)
    assert cmd.wait() == 4 #Check Return Code
    assert cmd.stdout.read ().decode ('utf-8') == "ERRO!: A máquina é identificada da seguinte maneira:\nX.X.X.X , sendo X um número entre 0 e 255\n"

# Testar ponta a ponta o programa, não acertando o número secreto
def test_connect ():
    port_id = random.randint(1200, 8000)
    Popen ("python3 server.py " + str(port_id), stdout = PIPE, shell=True)
    Popen ("python3 client.py testeId " + str(port_id), stdout = PIPE, shell=True) # máquina vai ser atribuída por defeito

