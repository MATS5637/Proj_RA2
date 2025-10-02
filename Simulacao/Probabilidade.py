import random
import numpy as np

class Probabilidade:
    @staticmethod
    def aleatorio_puro(quantidade: int = 200) -> list[int]:
        return [random.randint(1, 100) for _ in range(quantidade)]
    
    @staticmethod
    def aleatorio_poisson(quantidade: int = 200, lambda_P: float = 50.0) -> list[int]:
        numeros_poisson = np.random.poisson(lambda_P, quantidade)
        numeros_ajuste = np.clip(numeros_poisson, 1, 100)
        return [int(num) for num in numeros_ajuste]
    
    @staticmethod
    def aleatorio_ponderado(quantidade: int = 200) -> list[int]:
        textos_preferidos = list(range(30, 41))
        outros_textos = [i for i in range(1, 101) if i not in textos_preferidos]

        solicitacoes = []
        for _ in range(quantidade):
            if random.random() < 0.43:
                solicitacoes.append(random.choice(textos_preferidos))
            else:
                solicitacoes.append(random.choice(outros_textos))
        return solicitacoes
    
    @staticmethod
    def gerar_usuarios(num_usuarios=3, quantidade=200):
        return[{
            'usuario_id': i + 1,
            'solicitacoes': {
                'aleatorio_puro': Probabilidade.aleatorio_puro(quantidade),
                'aleatorio_poisson': Probabilidade.aleatorio_poisson(quantidade),
                'aleatorio_ponderado': Probabilidade.aleatorio_ponderado(quantidade)
            }
            } for i in range(num_usuarios)]
