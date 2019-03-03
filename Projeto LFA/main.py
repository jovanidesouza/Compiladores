from src.afnd import *
from src.minimiza import *
from src.determiniza import *
from src.auxi import *

afd = {}
alfabeto = []
gramatica = []

while True:#faz a leitura dos tokens do arquivo e chama função para gerar afnd
    try:
        token = input()
        if not token:
            break
        gerarAfndToken(afd, token, alfabeto)
    except EOFError:
        break

while True:#faz a leitura das regras da gramática e chama a função para gerar o afnd
    try:
        s = input()
        if not s:
            gerarAfndGramatica(afd, gramatica, alfabeto)
            gramatica.clear()
        else:
            gramatica.append(s)
    except EOFError:
        if gramatica:
            gerarAfndGramatica(afd, gramatica, alfabeto)
        break

eliminarEpsilonTransicoes(afd)#eliminas as epsilon transições do afnd
determinizar(afd)#transforma em afd
eliminarInalcancaveis(afd)#elimina os estados inalcançáveis
eliminarInuteis(afd)#elimina os mortos
exibirAutomatoDeterministico(afd, alfabeto)#printa na tela o AFD minimo
