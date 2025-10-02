class LRU:
    def __init__(self):
        self.capacidade = 10
        self.cache = {}
        self.utimo_uso = []
        self.hits = 0
        self.misses = 0

    def buscar_texto(self, numero_texto):
        if numero_texto in self.cache:
            self.hits += 1
            self.utimo_uso.remove(numero_texto)
            self.utimo_uso.append(numero_texto)
            return self.cache[numero_texto]
        else:
            self.misses += 1
            return None

    def adicionar_texto(self, numero_texto, texto):
        if numero_texto in self.cache:
            return
        if len(self.cache) >= self.capacidade:
            ultimo_usado = self.utimo_uso.pop(0)

            del self.cache[ultimo_usado]
        self.cache[numero_texto] = texto
        self.utimo_uso.append(numero_texto)
