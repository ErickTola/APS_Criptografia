import os
from hash import hash

def converte_txt_p_lista(texto_criptografado_raw):

    texto_criptografado = []
    texto_tmp = ''
    
    for i in texto_criptografado_raw:
        if i == '[' or (i == " "):
            continue
        elif i == ',':
            texto_criptografado.append(int(texto_tmp))
            texto_tmp = ''
            continue
        else:
            texto_tmp = texto_tmp + i
    return texto_criptografado

def converte_txt_p_dic(txt):

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
    i = 1
    total_votos = {'15': 0, '20': 0, '52': 0, '12': 0}
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
            hash_calculado = hash(bytes(texto_cript,'utf-8'))
            f = open(("Hash_numero_" +str(i)+".txt"), "r")
            hash_enviado = f.read()
            f.close
            
            if hash_enviado == hash_calculado:
                texto_cript = converte_txt_p_lista(texto_cript)
                chave = ler_chave()
                texto_descript = descriptografar(chave,texto_cript) + '}' 
                votos_tmp = converte_txt_p_dic(texto_descript)
                for j in total_votos:
                    total_votos[j] = votos_tmp[j] + total_votos[j]
            else :
                total_urnas_ignoradas = total_urnas_ignoradas + 1
                print("URNA NÚMERO",str(i),"COMPREMETIDA, VALOR DE HASH DIFERENTE. IGNORANDO ARQUIVO")
            
            i = i + 1

        if i > 100:
            if total_urnas == total_urnas_ignoradas:
                total_votos = "N/A"
            return total_votos

            

total_votos = abre_votos()

if total_votos != "N/A":
    Candidatos = {'15':'Marcos','20':'Silvio','52':'Marcela','12':'Claudia'}
    resultado = [kv[0] for kv in total_votos.items() if kv[1] == max(total_votos.values())]
    if len(resultado) <= 1:
        vencedor = Candidatos[resultado[0]]
        print(
            '''
                Bem vindo a votação de 2024!!!
                O total dos votos ficaram:

                Marcos: {0}
                Silvio: {1}
                Marcela: {2}
                Claudia: {3}

                {4} foi eleito para Presidente!!
            '''.format(total_votos['15'],total_votos['20'],total_votos['52'],total_votos['12'],vencedor)
            )
        
    elif len(resultado) > 1:
        print(
            '''
                Bem vindo a votação de 2024!!!
                O total dos votos ficaram:

                Marcos: {0}
                Silvio: {1}
                Marcela: {2}
                Claudia: {3}

                Ouve um empate!!!!
            '''.format(total_votos['15'],total_votos['20'],total_votos['52'],total_votos['12'])
            )
else:
    print("TODAS AS URNAS FORAM ADULTERADAS, ELEIÇÃO CANCELADA")