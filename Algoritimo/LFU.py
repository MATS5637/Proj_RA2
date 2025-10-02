class LFU:
    def __init__(self, capacidade=10):
        self.capacidade = capacidade
        self.cache = {}
        self.frequencia = {}
        self.hits = 0
        self.misses = 0


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
        
        if len(self.cache) >= self.capacidade:
            texto_menos_frequente = min(self.frequencia, key=self.frequencia.get)
            
            del self.cache[texto_menos_frequente]
            del self.frequencia[texto_menos_frequente]

        self.cache[numero_texto] = texto
        self.frequencia[numero_texto] = 0
          # Defina a capacidade da cache conforme necessário