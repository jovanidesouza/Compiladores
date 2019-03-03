TS = []

def verifica_cod_alfabeto(alfabeto):

    erro = False

    with open('codigo.txt') as cod_ref:
        for l_num, linha in enumerate(cod_ref, 1):
            y= linha.strip()
            for x in y:
                if x not in alfabeto and x != ' ':
                    print('Erro Léxico na linha:', l_num)
                    print('Na cadeia:',linha)
                    print('O caracter: "',x,'" não pertence ao alfabeto!\n')
                    erro = True

        return erro

def produz_tokens(afd):

    lista_nome = []
    lista_estado = []
    lista_linha = []
    erro = False

    with open('codigo.txt') as cod_ref:
        for l_num, linha in enumerate(cod_ref, 1):
            temp = linha.split()
            for x in range(len(temp)):
                lista_linha.append(l_num)
            lista_nome = lista_nome + temp
        print('\n\n')#até aqui ok, não mexer acima

    for l_num, token in enumerate(lista_nome, 0):
        estado_atual = 0 #todas as derivações inicial no estado 0 que é compartilhado
        for caracter in token:#passa por todos os caracters no token
            y = afd[estado_atual]
            if(caracter in y):
                c = y[caracter]
                estado_atual = int(''.join(map(str, c)))
            else:
                print('Erro lexico na linha: ', lista_linha[l_num], ': no token: ', token)
                erro = True
                #lista_nome[l_num] = '$' #sinalizar erro
                break
        if('@' not in afd[estado_atual]):
            print('Erro lexico na linha: ', lista_linha[l_num], ': no token: ', token)
            erro = True
            #lista_nome[l_num] = '$'
        else:
            lista_estado.append(estado_atual)

    if erro == True:
        return erro , lista_nome, TS
    #print('\t',lista_nome,'\n\t', lista_estado,'\n\t', lista_linha)

    #TS = []
    for x in range(len(lista_nome)):
        vet = [lista_nome[x], lista_estado[x], lista_linha[x]]
        TS.append(vet)
    print('TS:\n')
    for i in TS:
        print(i)
    print('\nFita de Saída\n')
    print(lista_nome)
    out_lex(TS)
    remove_lixo()

    return (erro , lista_nome, TS)

def get_ts():
    return TS
    #print(TS)

def out_lex(TS):
    #print('algo')
    with open('TS.txt', 'w') as arq:
        for linha in TS:
            print(linha, file=arq)

def remove_lixo():

    total = ''
    tex = []
    with open('TS.txt') as arq:
        for l_num, linha in enumerate(arq, 1):
            linha=linha.strip()
            linha=linha.strip('[')
            linha=linha.strip(']')
            linha=linha.replace(',','')
            linha=linha.replace("'",'')
            total = total + '\n' + linha
    with open('TS.txt', 'w') as arq:
        print(total, file=arq)
            #print(linha)
