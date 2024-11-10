def hash(arquivo):
    # Valores inicias do HASH, usamos uma constante do SHA-256 que são os primerios 32 bits dos decimais das raizes dos primeiros 8 números primos
    H = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

    # Outro grupo de constantes usadas no SHA-256, que são os primeiros 32 bits dos decimais das raizes cúbicas dos primeiros 64 números primos
    K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

    def rotacionar_direita(n, d):
        # Rotaciona para direita os bits inceridos (n) pelo número de vezes (d)   10000000000

        return (n >> d | n << (32 - d)) & 0xFFFFFFFF # 0XFFFFFFFF Garante que o resultado se mantenha á 32 bits. Isso será usado no código inteiro

    tamanho_byte = len(arquivo)
    tamanho_bit = tamanho_byte * 8

    # SHA-256 Trabalha com blocos de 512 bits, essa parte a baixo garante que se o arquivo for menor do que 512 bits, ele adiciona zeros para chegar a 512 bits.
    arquivo = arquivo + b'\x80'

    while (len(arquivo) * 8 + 64) % 512 != 0: # Adiciona bits "0" até chegar a 512 bits.
        arquivo = arquivo + b'\x00'
    arquivo = arquivo + tamanho_bit.to_bytes(8, 'big') # Adiciona o tamanho original da mensagem ao fim do bloco. 

    # Processa os blocos de 512 bits
    for i in range(0, len(arquivo), 64):
        bloco = arquivo[i:i+64]
        
        # Quebra o bloco em 16 linhas de 32 bits
        w = [int.from_bytes(bloco[j:j+4], 'big') for j in range(0, 64, 4)]
        
        # Cria mais 48 linhas de 32 bits a partir das 16 linhas iniciais
        for j in range(16, 64):
            s0 = rotacionar_direita(w[j-15], 7) ^ rotacionar_direita(w[j-15], 18) ^ (w[j-15] >> 3)
            s1 = rotacionar_direita(w[j-2], 17) ^ rotacionar_direita(w[j-2], 19) ^ (w[j-2] >> 10)
            w.append((w[j-16] + s0 + w[j-7] + s1) & 0xFFFFFFFF)

        a, b, c, d, e, f, g, h = H

        # Algoritimo principal

        for j in range(64):
            
            S1 = rotacionar_direita(e, 6) ^ rotacionar_direita(e, 11) ^ rotacionar_direita(e, 25)
            ch = (e & f) ^ ((~e) & g)
            numero_temp1 = (h + S1 + ch + K[j] + w[j]) & 0xFFFFFFFF
            S0 = rotacionar_direita(a, 2) ^ rotacionar_direita(a, 13) ^ rotacionar_direita(a, 22)
            maioria = (a & b) ^ (a & c) ^ (b & c)
            numero_temp2 = (S0 + maioria) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + numero_temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (numero_temp1 + numero_temp2) & 0xFFFFFFFF

        # Adiciona o bloco comprimido ao valor atual do HASH
        H[0] = (H[0] + a) & 0xFFFFFFFF
        H[1] = (H[1] + b) & 0xFFFFFFFF
        H[2] = (H[2] + c) & 0xFFFFFFFF
        H[3] = (H[3] + d) & 0xFFFFFFFF
        H[4] = (H[4] + e) & 0xFFFFFFFF
        H[5] = (H[5] + f) & 0xFFFFFFFF
        H[6] = (H[6] + g) & 0xFFFFFFFF
        H[7] = (H[7] + h) & 0xFFFFFFFF

    # Retorna o valor do Hash finalizado num tamanho de 256 bits
    return ''.join('{:08x}'.format(h) for h in H)

