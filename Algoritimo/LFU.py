import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Sistema.Cache import Cache

class LFU(Cache):
    def __init__(self, cap=10):
        super().__init__(cap)
        self.frequencia = {}

    def buscar_texto(self, numero_texto):
        if numero_texto in self.cache:
            self.frequencia[numero_texto] += 1
            self.hits += 1
            return self.cache[numero_texto]
        else:
            self.misses += 1
            return None

    def adicionar_texto(self, numero_texto, texto):
        if numero_texto in self.cache:
            return
        
        if len(self.cache) >= self.cap:
            texto_menos_frequente = min(self.frequencia, key=self.frequencia.get)
            
            del self.cache[texto_menos_frequente]
            del self.frequencia[texto_menos_frequente]

        self.cache[numero_texto] = texto
        self.frequencia[numero_texto] = 1
          # Defina a capacidade da cache conforme necessário