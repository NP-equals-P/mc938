# from . import AbstractGenerator
import numpy as np
import hashlib

class GolPRNGenerator():
    def __init__(self, initial_state, steps):
        super().__init__()
        self.state = initial_state
        self.steps = steps

    def generate_bytes(self, num_bytes):

        # --------- Calcular SHA256 da seed ---------
        if isinstance(self.state, int):
            # calcula o número mínimo de bytes necessários (pelo menos 1)
            length = max(1, (self.state.bit_length() + 7) // 8)
            state_bytes = self.state.to_bytes(length, 'big')
        elif isinstance(self.state, str):
            state_bytes = self.state.encode()
        elif isinstance(self.state, bytes):
            state_bytes = self.state
        else:
            # tenta converter coisas como bytearray ou iteráveis; caso falhe, usa a representação string
            try:
                state_bytes = bytes(self.state)
            except Exception:
                state_bytes = str(self.state).encode()
        digest_hex = hashlib.sha256(state_bytes).hexdigest()
        # -------------------------------------------

        # --------- Preparar a matriz inicial ---------
        bits_str = bin(int(digest_hex, 16))[2:].zfill(256)
        bits = np.fromiter((int(b) for b in bits_str), dtype=int)
        matriz = bits.reshape((16, 16))
        original = matriz.copy()
        # ---------------------------------------------

        resultado = np.zeros(num_bytes*8, dtype=int)

        for i in range(num_bytes*8):

            if (i % self.steps) == 1:
                matriz = matriz ^ original

            matriz, celulas_mortas = self.update_state(matriz)

            if celulas_mortas % 2 == 0:
                resultado[i] = 0
            else:
                resultado[i] = 1

        return resultado
    
    def update_state(self, matriz):

        matriz = np.array(matriz, dtype=int)
        
        linhas, colunas = matriz.shape
        
        proximo_estado = np.zeros_like(matriz)
        
        celulas_mortas = 0

        for i in range(linhas):
            for j in range(colunas):

                vizinhos_vivos = 0
                
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        
                        vizinho_i = (i + di) % linhas
                        vizinho_j = (j + dj) % colunas
                        
                        vizinhos_vivos += matriz[vizinho_i, vizinho_j]
                
                if matriz[i, j] == 1: 
                    if vizinhos_vivos == 2 or vizinhos_vivos == 3:
                        proximo_estado[i, j] = 1  
                    else:
                        proximo_estado[i, j] = 0  

                        celulas_mortas += 1
                else: 
                    if vizinhos_vivos == 3:
                        proximo_estado[i, j] = 1  
                    else:
                        proximo_estado[i, j] = 0 
        
        return proximo_estado, celulas_mortas
    
if __name__ == "__main__":

    gol = GolPRNGenerator(831321112, steps=3)
    print(gol.generate_bytes(16))