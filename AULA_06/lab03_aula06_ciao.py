# Laboratório 03 — Completando o ACO
import random
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CUSTOS = np.array([
    [0, 2, 4, np.inf, np.inf, np.inf],
    [2, 0, 1, 5, np.inf, np.inf],
    [4, 1, 0, 2, 3, np.inf],
    [np.inf, 5, 2, 0, 1, 4],
    [np.inf, np.inf, 3, 1, 0, 2],
    [np.inf, np.inf, np.inf, 4, 2, 0]
], dtype=float)
ORIGEM, DESTINO = 0, 5
NUM_FORMIGAS, NUM_ITERACOES = 20, 50
ALPHA, BETA = 1.0, 2.0
TAXA_EVAPORACAO, Q = 0.5, 100.0

def obter_vizinhos(no):
    return [p for p in range(len(CUSTOS)) if p != no and np.isfinite(CUSTOS[no, p])]

def calcular_custo(rota):
    return sum(CUSTOS[a, b] for a, b in zip(rota, rota[1:]))

def executar_aco(seed=42, num_formigas=NUM_FORMIGAS, num_iteracoes=NUM_ITERACOES, alpha=ALPHA, beta=BETA, taxa_evaporacao=TAXA_EVAPORACAO):
    rng = random.Random(seed)
    feromonio = np.where(np.isfinite(CUSTOS), 1.0, 0.0)
    melhor_rota, melhor_custo, historico = None, float('inf'), []
    def construir_rota():
        rota, atual = [ORIGEM], ORIGEM
        while atual != DESTINO:
            candidatos = [p for p in obter_vizinhos(atual) if p not in rota]
            if not candidatos: return None
            atr = [feromonio[atual, p] ** alpha * (1 / CUSTOS[atual, p]) ** beta for p in candidatos]
            proximo = rng.choices(candidatos, weights=atr, k=1)[0]
            rota.append(proximo); atual = proximo
        return rota
    for _ in range(num_iteracoes):
        rotas = []
        for _ in range(num_formigas):
            rota = construir_rota()
            if rota is not None:
                custo = calcular_custo(rota); rotas.append((rota, custo))
                if custo < melhor_custo: melhor_rota, melhor_custo = rota.copy(), custo
        feromonio *= (1 - taxa_evaporacao)
        feromonio[~np.isfinite(CUSTOS)] = 0
        for rota, custo in rotas:
            deposito = Q / custo
            for a, b in zip(rota, rota[1:]): feromonio[a, b] += deposito
        historico.append(melhor_custo)
    return melhor_rota, melhor_custo, historico, feromonio

feromonio = np.where(np.isfinite(CUSTOS), 1.0, 0.0)

def calcular_atratividade(no_atual, proximo):
    fer = feromonio[no_atual, proximo]
    custo = CUSTOS[no_atual, proximo]
    return fer ** ALPHA * (1 / custo) ** BETA

def evaporar_feromonio():
    global feromonio
    feromonio *= (1 - TAXA_EVAPORACAO)
    feromonio[~np.isfinite(CUSTOS)] = 0

def depositar_feromonio(rota, custo):
    deposito = Q / custo
    for origem, destino in zip(rota, rota[1:]): feromonio[origem, destino] += deposito

def construir_rota():
    rota, atual = [ORIGEM], ORIGEM
    while atual != DESTINO:
        candidatos = [p for p in obter_vizinhos(atual) if p not in rota]
        if not candidatos: return None
        atratividades = [calcular_atratividade(atual, p) for p in candidatos]
        probabilidades = np.array(atratividades) / sum(atratividades)
        proximo = random.choices(candidatos, weights=probabilidades, k=1)[0]
        rota.append(proximo); atual = proximo
    return rota

if __name__ == '__main__':
    random.seed(42); melhor_rota, melhor_custo = None, float('inf')
    for _ in range(NUM_ITERACOES):
        rotas = []
        for _ in range(NUM_FORMIGAS):
            rota = construir_rota()
            if rota is not None:
                custo = calcular_custo(rota); rotas.append((rota, custo))
                if custo < melhor_custo: melhor_rota, melhor_custo = rota.copy(), custo
        evaporar_feromonio()
        for rota, custo in rotas: depositar_feromonio(rota, custo)
    print('Melhor rota:', melhor_rota); print('Melhor custo:', melhor_custo)
