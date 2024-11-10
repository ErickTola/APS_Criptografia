import os
from hash import hash

def converte_txt_p_lista(texto_criptografado_raw):
    # Converte um aquivo de texto para número e o anexa a uma lista
    texto_criptografado = []
    texto_tmp = ''
    
    for i in texto_criptografado_raw:
        if i == '[' or (i == " "):
            continue
        elif i == ',' or i == ']':
            texto_criptografado.append(int(texto_tmp))
            texto_tmp = ''
            continue
        else:
            texto_tmp = texto_tmp + i
    return texto_criptografado

def converte_txt_p_dic(txt):
    #Converte de texto para um dicionário
    lista = []
    texto_tmp = ''

    for i in txt:
        if i == '{' or (i == " ") or i == "'":
            continue
        elif i == '}' or i == ',':
            x = texto_tmp.split(':')
            x[1] = int(x[1])
            lista.append(x)
            texto_tmp = ''
        else:
            texto_tmp = texto_tmp + i

    return dict(lista)

def ler_chave():
    # Lê a chave privada e a converte para número
    f = open("Chave_privada.txt", 'r')
    chave_lida = f.read()
    f.close()

    numero1 = ''
    numero2 = ''
    parte2 = False
    for i in chave_lida:
        if i == '(' or i == ')' or (i == " "):
            continue
        elif i == ',':
            parte2 = True
            continue
        if not parte2:
            numero1 = numero1 + i
        else:
            numero2 = numero2 + i
    return (int(numero1),int(numero2))

def descriptografar(chave_privada, texto_criptografado):

    d, n = chave_privada
    #Descriptografa cada número para o valor original e converte para texto no padrão UTF-8
    texto = ''.join([chr((char ** d) % n) for char in texto_criptografado])
    return texto

def abre_votos():
    #Abre o arquivo de cada urna e soma os votos
    i = 1
    votos = {'15': 0, '20': 0, '52': 0, '12': 0, '00' : 0, 'NULL' : 0}
    total_urnas = 0
    total_urnas_ignoradas = 0


    while True:
        if not os.path.isfile("Urna_numero_" +str(i)+"_votos.txt"):
            i = i + 1
        else:
            total_urnas = total_urnas + 1
            f = open(("Urna_numero_" +str(i)+"_votos.txt"), "r")
            texto_cript = f.read()
            f.close
            #Calcula o Hash do arquivo aberto e compara com o hash original enviado
            hash_calculado = hash(bytes(texto_cript,'utf-8'))
            f = open(("Hash_numero_" +str(i)+".txt"), "r")
            hash_enviado = f.read()
            f.close
            
            if hash_enviado == hash_calculado:
                texto_cript = converte_txt_p_lista(texto_cript)
                chave = ler_chave()
                texto_descript = descriptografar(chave,texto_cript) 
                votos_tmp = converte_txt_p_dic(texto_descript)
                for j in votos:
                    votos[j] = votos_tmp[j] + votos[j]
            else :
                #Caso o hash seja diferente do original, ele nega a leitura do arquivo e o ignora na contagem
                total_urnas_ignoradas = total_urnas_ignoradas + 1
                print("URNA NÚMERO",str(i),"COMPREMETIDA, VALOR DE HASH DIFERENTE. IGNORANDO ARQUIVO")
            
            i = i + 1

        #Termina o processo de leitura
        if i > 100:
            if total_urnas == total_urnas_ignoradas:
                votos = "N/A"
            return votos

def decript_relatorio():
    #Descriptografa os relatórios enviados das urnas para a leitura individual
    w = 1
    while True:
        if not os.path.isfile("Relatório_Urna_" +str(w)+"Cript.txt"):
            w = w + 1
        else:
                f = open("Relatório_Urna_" +str(w)+"Cript.txt", "r")
                texto_raw = f.read()
                f.close()
                f = open("Relatório_Urna_" +str(w)+"Descript.txt", "w")
                texto_cript = converte_txt_p_lista(texto_raw)

                hash_calculado = hash(bytes(texto_raw,'utf-8'))
                v = open(("Hash_Relatório_" +str(w)+".txt"), "r")
                hash_enviado = v.read()
                v.close

                if hash_enviado == hash_calculado:

                    chave = ler_chave()
                    texto_descript = descriptografar(chave,texto_cript) 
                    f.write(texto_descript)
                    f.close()

                else :
                    #Caso o hash seja diferente do original, ele nega a leitura do arquivo e o ignora na contagem
                    print("RELATÓRIO NÚMERO",str(w),"COMPREMETIDA, VALOR DE HASH DIFERENTE. IGNORANDO ARQUIVO")

                w = w + w


        if w > 100:
                break
            
total_votos = 0
votos = abre_votos()
for i in votos:
    total_votos = total_votos + votos[i]
decript_relatorio()
f = open("Total_Votos_Apurados.txt", "w")
f.write(
'''
    APURAÇÃO DE VOTOS:

    Os votos foram:

    Marcos: {0}
    Silvio: {1}
    Marcela: {2}
    Claudia: {3}
    Branco: {4}
    Nulo: {5}

    TOTAL DE VOTOS: {6}


'''.format(votos['15'],votos['20'],votos['52'],votos['12'],votos['00'],votos['NULL'],total_votos)
)