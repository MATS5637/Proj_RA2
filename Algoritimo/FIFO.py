import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Sistema.Cache import Cache

class FIFO(Cache):
    def __init__(self, cap=10):
        super().__init__(cap)
        self.fila = []

    def buscar_texto(self, numero_texto):
            return self.cache.get(numero_texto, None)

    def adicionar_texto(self, numero_texto, texto):
        if numero_texto in self.cache:
            return  
        
        if len(self.cache) >= self.cap:
            texto_removido = self.fila.pop(0)
            del self.cache[texto_removido]

        self.cache[numero_texto] = texto
        self.fila.append(numero_texto)
