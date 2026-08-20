# Atividade 3 — Heurística Gulosa + Cálculo do Gap de Otimalidade
import numpy as np
import itertools


def mochila_otima(pesos, valores, capacidade):
    """Retorna o maior valor possível por enumeração completa."""
    n = len(pesos)
    melhor = 0
    for combinacao in itertools.product([0, 1], repeat=n):
        peso = sum(pesos[i] for i in range(n) if combinacao[i])
        if peso <= capacidade:
            valor = sum(valores[i] for i in range(n) if combinacao[i])
            melhor = max(melhor, valor)
    return melhor


def mochila_gulosa(pesos, valores, capacidade):
    """Seleciona itens pela maior densidade valor/peso enquanto houver espaço."""
    densidade = sorted(((valores[i] / pesos[i], i) for i in range(len(pesos))), reverse=True)
    valor_total = 0
    peso_atual = 0
    for _, indice in densidade:
        if peso_atual + pesos[indice] <= capacidade:
            peso_atual += pesos[indice]
            valor_total += valores[indice]
    return valor_total


def calcular_gap(valor_heuristica, valor_otimo):
    """Calcula a diferença percentual entre a heurística e o ótimo."""
    if valor_otimo == 0:
        return 0.0
    return ((valor_otimo - valor_heuristica) / valor_otimo) * 100


np.random.seed(42)
n_itens = 12
capacidade = 30
n_instancias = 20
gaps = []

print('Rodando', n_instancias, 'instâncias...')
for k in range(n_instancias):
    pesos = np.random.randint(1, 15, size=n_itens)
    valores = np.random.randint(10, 50, size=n_itens)
    otimo = mochila_otima(pesos, valores, capacidade)
    heuristica = mochila_gulosa(pesos, valores, capacidade)
    gap = calcular_gap(heuristica, otimo)
    gaps.append(gap)
    print(f'Instância {k + 1:2d} | Ótimo: {otimo:4d} | Gulosa: {heuristica:4d} | Gap: {gap:5.1f}%')

print('\n===== RESUMO =====')
print(f'Gap médio     : {np.mean(gaps):.2f}%')
print(f'Gap mínimo     : {np.min(gaps):.2f}%')
print(f'Gap máximo     : {np.max(gaps):.2f}%')
print(f'Desvio padrão : {np.std(gaps):.2f}%')
