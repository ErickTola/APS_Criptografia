import random

def mdc(a, b):
    #Calcula o maior divisor comum usando o algoritimo euclidiano
    while b != 0:

        c = a % b
        a = b 
        b = c
    return a

def e_primo(n):
    #Checa se um número é primo
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6
    return True

def gera_numero_primo():
    #Gera um número primo
    while True:
        numero = random.randint(101, 1000)
        if e_primo(numero):
            return numero

def mdc_extendido(a, m):
    # Executa o algoritimo extendido de Euclides

    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def gera_chaves():
    #Gera uma chave pública e uma chave privada

    p = gera_numero_primo()
    q = gera_numero_primo()
    
    n = p * q
    phi = (p - 1) * (q - 1)

    # Escolhe um inteiro "e" de tal modo que 1 < e < phi e mdc(e, phi) = 1
    e = random.randint(2, phi - 1)
    while mdc(e, phi) != 1:
        e = random.randint(2, phi - 1)

    # Calcula o modulo inverso de "e"
    d = mdc_extendido(e, phi)
    
    # Retorna a chave Pública (e, n) e a chave Privada (d, n)
    return ((e, n), (d, n))

def criptografar(chave_publica, texto):

    e, n = chave_publica
    #Converte cada letra no texto para um numero no padrão UTF-8 e criptografa
    texto_criptografado = [(ord(char) ** e) % n for char in texto]

    return texto_criptografado

def descriptografar(chave_privada, texto_criptografado):
    
    d, n = chave_privada
    #Descriptografa cada número para o valor original e converte para texto no padrão UTF-8
    texto = ''.join([chr((char ** d) % n) for char in texto_criptografado])
    return texto

chave_publica, chave_privada = gera_chaves()

f = open("Chave_publica.txt", 'w')
f.write(str(chave_publica))
f.close()

f = open("Chave_privada.txt", 'w')
f.write(str(chave_privada))
f.close()