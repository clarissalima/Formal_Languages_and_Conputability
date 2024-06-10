# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

if len(sys.argv) <= 1:
    print("Passe o caminho do arquivo de teste corretamente.")
    exit()
file_to_open = sys.argv[1]

with open(file_to_open) as file:
    Lines = file.readlines()

Lines.remove('\n')
Lines.remove('producoes\n')

prod_list = [] 
variables = None # list with non terminals symbols
initial_var = None
terminals = None
productions = {}

# get variables from file

for line in Lines:
    # to remove every tab, space and new line
    line = re.sub(r'[\n\t\s]*', '', line)

    if line.startswith('variaveis'):
        line = line.replace('variaveis','')
        line = line.replace(':','')
        variables = line.split(',')

    elif line.startswith('inicial'):
        initial_var = line.replace('inicial','')
        initial_var = initial_var.replace(':','')

    elif line.startswith('terminais'):
        terminals = line.strip()
        terminals = terminals.replace('terminais','')
        terminals = terminals.replace(':','')
        terminals = terminals.split(',')
    elif line:
        prod_list.append(line.strip())
    else:
        continue

# Verifying if all characters in productions are valid
# turn off when it has ascii problems
'''
for prod in prod_list:
    test_prod = prod.split(':')
    for item in test_prod:
        if item == 'epsilon' or (item in variables) or (item in terminals):
            continue
        else:
            for char in item:
                if char == ':' or (char in variables) or (char in terminals):
                    continue
                else:
                    print(char)
                    print('Erro nas escrita das producoes.')
                    exit()

'''

prod_list = tuple(prod_list)

for prod in prod_list:
    if prod.startswith(prod_list):
        prod = prod.split(':')
        productions.setdefault(prod[0], [])
        productions[prod[0]].append(prod[1])

def validEntries():
    output = True

    if len(variables) < 1:
       print('Erro nas variaveis.')
       output = False
    else:
        for i in variables:
            if i.isalpha() and i.isupper():
                continue
            else:
                print('Erro nas variaveis.')
                output = False

    if (not initial_var.isalpha()) and (not initial_var.isupper()) and (not(initial_var in variables)) and (not len(initial_var) == 1):
       print('Erro no nao terminal inicial.')
       output = False

    if len(terminals) < 1:
       print('Erro nos terminais.')
    else:
        for i in terminals:
            if (i.isalpha() and i.islower()) or i.isdigit:
                continue
            else:
                print('Erro nos terminais.')
                output = False

    keylist = []
    for key in productions.keys():
        keylist.append(key)
        if key not in variables:
            print('Nao terminal do lado esquerdo nao presente em variaveis declaradas.')
            output = False

    if len(keylist) != len(variables):
        print('Erro nas produções.')
        output = False

    return output

# FAST MODE

def fast_mode():
    chain_possibility = []
    ends_possibility = []
    for x in productions:
        for y in productions[x]:
            if y == "epsilon":
                chain_possibility.append(x)
                ends_possibility.append(y)
                continue

            is_end_possibility = True
            for i in y:
                if i in variables:
                  is_end_possibility = False
            if is_end_possibility:
                chain_possibility.append(x)
                ends_possibility.append(y)

    continue_fast_mode = True
    k = 0
    while continue_fast_mode:
        chain = ""
        chain_path = []
        if k == len(chain_possibility):
            k = 0
        chain_path.append(ends_possibility[k])
        chain_path.append(chain_possibility[k])
        k += 1
        i = 1
        while chain_path[i] != initial_var:
            for x in productions:
                for y in productions[x]:
                    if chain_path[i] in y:
                        chain_path.append(x)
                        i += 1
                        break
                if chain_path[i] == initial_var:
                    break

        print("Derivacao:")
        chain_sub_str = []
        chain_sub_str.append(str(chain_path[len(chain_path) - 1]) + " -> ")
        chain += chain_sub_str[0]
        j = 0
        for i in range(len(chain_path)-1, 0, -1):
            for x in productions[chain_path[i]]:
                if chain_path[i - 1] in x:
                    match = re.search(r'(.*?)(?= ->)', chain_sub_str[j])
                    if match:
                        if "epsilon" == x:
                            x = ""
                        aux = match.group(0).replace(chain_path[i], x, 1)
                        chain_sub_str.append(aux + " -> ")
                        j += 1
                        chain += chain_sub_str[j]
                    break;

        print(chain[:-4])
        print("Cadeia gerada:")
        print(chain_sub_str[len(chain_sub_str) - 1][:-4])

        print("\nDeseja gerar outra cadeia? (s/n)")
        keep = input()
        if keep.lower() != 's':
            continue_fast_mode = False


# DETAILED MODE
def detailed_mode():
    chain_sub_str = initial_var + " -> "
    chain = chain_sub_str
    current_variable = None
    print("Derivacao:")
    print(chain)

    while any(j in variables for j in chain_sub_str):
        for i in chain_sub_str:
          if i.isupper():
            current_variable = i
            break
        print(f"\nEscolha a operacao de {current_variable}: ")
        print(productions[current_variable])
        operation = input()
        operacao_valida = False
        for x in productions[current_variable]:
            if operation in x:
                operacao_valida = True
                break
        if operacao_valida:
            match = re.search(r'(.*?)(?= ->)', chain_sub_str)
            if match:
                if operation == "epsilon":
                  operation = ""
                aux = match.group(0).replace(current_variable, operation, 1)
                chain_sub_str = aux + " -> "
                chain += chain_sub_str
                print(chain[:-4])
        else:
            print("Operacao invalida!")

    print("\nCadeia gerada:")
    print(chain_sub_str[:-4])


# MENU 

running = True
while running:
    print('\n----- Gerador de Cadeias para Gramaticas Livres de Contexto -----\n')

    validation = validEntries()

    if validation == True:
        print('Producoes:')
        print(productions)
        print('\nSelecione o modo como a GLC gera:')
        print('1. Modo rapido')
        print('2. Modo detalhado')
        print('3. Sair')

        menu = input()

        if menu == '1':
            print ('\n--- Modo Rapido ---')
            fast_mode()
        if menu == '2':
            print ('\n--- Modo Detalhado ---')
            detailed_mode()
        if menu == '3':
           running = False

    else:
        print('Existem erros no arquivo de entrada!')
        running = False
