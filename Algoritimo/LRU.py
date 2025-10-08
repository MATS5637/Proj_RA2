import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Sistema.Cache import Cache

class LRU(Cache):
    def __init__(self, cap=10):
        super().__init__(cap)
        self.ultimo_uso = []

    def buscar_texto(self, numero_texto):
        if numero_texto in self.cache:
            self.hits += 1
            self.ultimo_uso.remove(numero_texto)
            self.ultimo_uso.append(numero_texto)
            return self.cache[numero_texto]
        else:
            self.misses += 1
            return None

    def adicionar_texto(self, numero_texto, texto):
        if numero_texto in self.cache:
            self.ultimo_uso.remove(numero_texto)
            self.ultimo_uso.append(numero_texto)
            return
        if len(self.cache) >= self.cap:
            ultimo_usado = self.ultimo_uso.pop(0)
            del self.cache[ultimo_usado]

        self.cache[numero_texto] = texto
        self.ultimo_uso.append(numero_texto)
