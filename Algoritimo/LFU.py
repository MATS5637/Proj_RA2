import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from Sistema.Cache import Cache

class LFU(Cache):
    def __init__(self, cap=10):
        super().__init__(cap)
        self.frequencia = {}

    def buscar_texto(self, numero_texto):
            return self.cache.get(numero_texto, None)

    def adicionar_texto(self, numero_texto, texto):
        if numero_texto in self.cache:
            self.frequencia[numero_texto] += 1
            return
        
        if len(self.cache) >= self.cap:
            min_frequencia = min(self.frequencia.values())
            candidatos = [k for k, v in self.frequencia.items() if v == min_frequencia]
            texto_remover = candidatos[0]
            
            del self.cache[texto_remover]
            del self.frequencia[texto_remover]

        self.cache[numero_texto] = texto
        self.frequencia[numero_texto] = 1
