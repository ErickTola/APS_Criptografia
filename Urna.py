import os
from hash import hash

def salva_votos(resultado):
    # Pega o resultado dos votos criptografados e salva em um arquivo de texto
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

def salva_relatorio(sequencia,chave_pub):
    # Pega o resultado dos votos e cria um relatório com a sequencia de votos, votos para os candidatos e total de votos e o criptografa
    j = 1
    while True:
        if os.path.isfile("Relatório_Urna_" +str(j)+"Cript.txt"):
                j = j + 1
        else:
            

            relatorio = ('''Relatório de votos:
                        
Urna número {0}

Sequencia de votos:\n'''.format(j))

            for h in range(0,len(sequencia)):
                relatorio = relatorio + "\n" + ("{0} - {1}".format(h+1,sequencia[h]))

            relatorio = relatorio + "\n \n" + "Total de Votos: " + str(len(sequencia))

            for k in range(len(votos)):
                relatorio = relatorio + "\n" + candidatos[k] + ": " + str(votos[candidatos_id[k]])
            
            f = open("Relatório_Urna_" +str(j)+"Cript.txt", "w")
            relatorio_crip = (str(criptografar(chave_pub,relatorio)))
            f.write(relatorio_crip)
            f.close
            f = open(("Hash_Relatório_" +str(j)+".txt"), "w")
            f.write(str(hash(bytes(relatorio_crip,"utf-8"))))
            f.close
            break


def criptografar(chave_publica, texto):

    e, n = chave_publica
    #Converte cada letra no texto para um numero no padrão UTF-8 e criptografa
    texto_criptografado = [(ord(char) ** e) % n for char in texto]

    return texto_criptografado

def ler_chave():
    #Abre a chave Pública para poder criptografar o resultado
    f = open("Chave_publica.txt", 'r')
    chave_lida = f.read()
    f.close()

    numero1 = ''
    numero2 = ''
    parte2 = False
    # Converte o texto do arquivo para número e o anexa a uma lista
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

#Define os candidatos e seus IDs
votos = {"15":0,"20":0,"52":0,"12":0,"00": 0, "NULL": 0}
candidatos = ["Marcos","Silvio","Marcela","Claudia","Branco","Nulo"]
candidatos_id = ["15","20","52","12","00","NULL"]
Continuar = 'S'
sequencia = []

#Inicia o algoritimo de votação
while Continuar[:1] == 'S' or Continuar[:1] == 's':
    print(
    '''
        Bem vindo a votação de 2024!!!
        Suas opções de canditados são:

        Marcos (15)
        Silvio (20)
        Marcela (52)
        Claudia (12)
        Branco (00)
    '''
    )
    
    while True:
        try:
                voto = int(input("Digite o número do candidato que você quer eleger: "))
                break
        except:
                voto = "nulo"
                break


    if voto == 15:
        voto = 0
    elif voto == 20:
        voto = 1
    elif voto == 52:
        voto = 2
    elif voto == 12:
        voto = 3
    elif voto == 00:
        voto = 4
    elif voto == "nulo":
        voto = 5
    else:
        voto = 5
 
    
    print("Você selecionou",candidatos[voto],"Quer confirmar? (S/N): ")
    conf = input()
    # Verifica se o voto é nulo ou branco
    if voto == 4 or voto == 5:
        if conf[:1] == 'S' or conf[:1] == 's':
            print("Você votou", candidatos[voto]+"!!!")
            sequencia.append(candidatos[voto])
            votos[candidatos_id[voto]] = votos[candidatos_id[voto]] + 1
            restart = input("Continuar Votando? (S/N): ")
            if restart == 's' or restart == 'S':
                continue
            else:
                break
        else:
            continue
    else:
        if conf[:1] == 'S' or conf[:1] == 's':
            print("Você votou no(a)", candidatos[voto]+"!!!")
            sequencia.append(candidatos[voto])
            votos[candidatos_id[voto]] = votos[candidatos_id[voto]] + 1
            restart = input("Continuar Votando? (S/N): ")
            if restart[:1] == 's' or restart[:1] == 'S':
                continue
            else:
                break
        else:
            continue
        

chave_pub = ler_chave()
texto_cript = criptografar(chave_pub, str(votos))
salva_votos(texto_cript)
salva_relatorio(sequencia,chave_pub)

