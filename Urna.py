import os
from hash import hash

def salva_votos(resultado):
    i = 1
    while True:
        if os.path.isfile("Urna_numero_" +str(i)+"_votos.txt"):
            i = i + 1
        else:
            resultado_str = str(resultado)
            f = open(("Urna_numero_" +str(i)+"_votos.txt"), "w")
            f.write(resultado_str)
            f.close
            f = open(("Hash_numero_" +str(i)+".txt"), "w")
            f.write(str(hash(bytes(resultado_str,"utf-8"))))
            f.close
            break


def criptografar(chave_publica, texto):

    e, n = chave_publica
    #Converte cada letra no texto para um numero no padrão UTF-8 e criptografa
    texto_criptografado = [(ord(char) ** e) % n for char in texto]

    return texto_criptografado

def ler_chave():

    f = open("Chave_publica.txt", 'r')
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

votos = {"15":0,"20":0,"52":0,"12":0}
candidatos = ["Marcos","Silvio","Marcela","Claudia"]
candidatos_id = ["15","20","52","12"]
Continuar = 'S'

while Continuar[:1] == 'S' or Continuar[:1] == 's':
    print(
    '''
        Bem vindo a votação de 2024!!!
        Suas opções de canditados são:

        Marcos (15)
        Silvio (20)
        Marcela (52)
        Claudia (12)
    '''
    )
    
    while True:
        try:
                voto = int(input("Digite o número do candidato que você quer eleger: "))
                break
        except:
                print("\nNúmero inválido, digite novamente")
                print(
                '''
                    Bem vindo a votação de 2024!!!
                    Suas opções de canditados são:

                    Marcos (15)
                    Silvio (20)
                    Marcela (52)
                    Claudia (12)
                '''
                )

    if voto == 15:
        voto = 0
    elif voto == 20:
        voto = 1
    elif voto == 52:
        voto = 2
    elif voto == 12:
        voto = 3
    else: 
        print("\nNúmero inválido, digite novamente")
        continue

    print("Você selecionou",candidatos[voto],"Quer confirmar? (S/N): ")
    conf = input()
    if conf[:1] == 'S' or conf[:1] == 's':
        print("Você votou no(a)", candidatos[voto]+"!!!")
        votos[candidatos_id[voto]] = votos[candidatos_id[voto]] + 1
        restart = input("Continuar Votando? (S/N): ")
        if restart == 's' or restart == 'S':
            continue
        else:
            break
    else:
        continue

chave_pub = ler_chave()
texto_cript = criptografar(chave_pub, str(votos))
salva_votos(texto_cript)



