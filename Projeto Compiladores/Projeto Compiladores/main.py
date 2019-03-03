from src.afnd import *
from src.minimiza import *
from src.determiniza import *
from src.auxi import *
from src.lexico import *
#from lexclass import *
#from src.sintatico import *

afd = {}
alfabeto = []
gramatica = []

while True:#faz a leitura dos tokens no arquivo de entrada
    try:
        token = input()
        if not token:
            break
        gerarAfndToken(afd, token, alfabeto)
    except EOFError:
        break

while True:#faz a leitura das regras da GR no arquivo de entrada
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
#gera dois afnds separados e depois faz a união dos dois

eliminarEpsilonTransicoes(afd)
determinizar(afd)
eliminarInalcancaveis(afd)
eliminarInuteis(afd)
##################################
#fim do trabalho de LFA#
##################################
Fita = []#fita de saida da analise lexica
TabelaSimbolos = []
print('\nAlfabeto da linguagem hipotética:\n')
print(alfabeto)
#print('\nAFD:\n')
#exibirAutomatoDeterministico(afd, alfabeto)
print('\n\nANÁLISE LÉXICA:\n')
pdPASS = True #booleao para verificar aceitação das análises
pdPASS = verifica_cod_alfabeto(alfabeto)#verifica o codigo com o alfabeto
if pdPASS == False:
    pdPASS , Fita , TabelaSimbolos = produz_tokens(afd)#faz a analise lexica e gera a TS
if pdPASS == False:#se False, então a analise lexica foi concluida sem erros
    print('\nLéxica OK!\nPronto para a análise sintática\n')
    from src.sintatico import *
    pdPASS = a_sintatica(Fita, TabelaSimbolos)#inicia a analise sintatica
if pdPASS == False:#se false, nenhum erro sintatico foi encontrado
    print('\nfim da análise sintática\n')
    #pdPASS = a_semantica()
#get_ts()
