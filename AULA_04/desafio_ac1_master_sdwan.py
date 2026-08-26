"""
Desafio de Fechamento AC-1 — Motor de Decisioning SD-WAN Zero-Trust.

Relatório técnico: o motor avalia rotas entre o nó 0 e o nó 11 usando uma
função de fitness ponderada por latência e perda de pacotes. Qualquer rota que
passe por um roteador com reputação inferior a 50 recebe penalização fixa de
5.000 pontos; por isso, o resultado reporta explicitamente os nós evitados e
os nós não confiáveis presentes na topologia.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

NUM_NOS = 12
ORIGEM = 0
DESTINO = 11
NUM_INTERMEDIARIOS = 4
TAMANHO_POPULACAO = 120
NUM_GERACOES = 300
TAXA_MUTACAO = 0.15
PENALIDADE_SEGURANCA = 5000.0
LIMIAR_REPUTACAO = 50.0
PESO_LATENCIA = 1.0
PESO_PERDA = 20.0
SEMENTE = 2026


@dataclass(frozen=True)
class Topologia:
    adjacencia: np.ndarray
    latencia: np.ndarray
    perda: np.ndarray
    reputacao: np.ndarray


@dataclass(frozen=True)
class Resultado:
    rota: np.ndarray
    latencia_total: float
    perda_total: float
    penalidade_seguranca: float
    fitness: float
    nos_nao_confiaveis: list[int]
    historico: list[float]


def criar_topologia(semente: int = SEMENTE) -> Topologia:
    """Gera uma topologia completa e simétrica de 12 roteadores."""
    rng = np.random.default_rng(semente)
    adjacencia = np.ones((NUM_NOS, NUM_NOS), dtype=bool)
    np.fill_diagonal(adjacencia, False)
    latencia = rng.uniform(8.0, 80.0, (NUM_NOS, NUM_NOS))
    latencia = (latencia + latencia.T) / 2
    perda = rng.uniform(0.05, 8.0, (NUM_NOS, NUM_NOS))
    perda = (perda + perda.T) / 2
    np.fill_diagonal(latencia, 0.0)
    np.fill_diagonal(perda, 0.0)
    reputacao = rng.integers(25, 96, size=NUM_NOS).astype(float)
    reputacao[ORIGEM] = max(reputacao[ORIGEM], 70.0)
    reputacao[DESTINO] = max(reputacao[DESTINO], 70.0)
    return Topologia(adjacencia, latencia, perda, reputacao)


def validar_rota(rota: np.ndarray, topologia: Topologia) -> None:
    if len(rota) != NUM_INTERMEDIARIOS + 2:
        raise ValueError("A rota deve conter origem, quatro intermediários e destino.")
    if int(rota[0]) != ORIGEM or int(rota[-1]) != DESTINO:
        raise ValueError("A rota deve começar no nó 0 e terminar no nó 11.")
    if len(set(map(int, rota))) != len(rota):
        raise ValueError("A rota não pode repetir roteadores.")
    if not all(topologia.adjacencia[int(a), int(b)] for a, b in zip(rota[:-1], rota[1:])):
        raise ValueError("A rota contém um enlace inexistente.")


def calcular_metricas(rota: np.ndarray, topologia: Topologia) -> tuple[float, float]:
    validar_rota(rota, topologia)
    enlaces = list(zip(rota[:-1], rota[1:]))
    latencia = float(sum(topologia.latencia[int(a), int(b)] for a, b in enlaces))
    perda = float(sum(topologia.perda[int(a), int(b)] for a, b in enlaces))
    return latencia, perda


def calcular_fitness(rota: np.ndarray, topologia: Topologia) -> float:
    latencia, perda = calcular_metricas(rota, topologia)
    nos_inseguros = [int(no) for no in rota if topologia.reputacao[int(no)] < LIMIAR_REPUTACAO]
    penalidade = PENALIDADE_SEGURANCA if nos_inseguros else 0.0
    return PESO_LATENCIA * latencia + PESO_PERDA * perda + penalidade


def criar_populacao(rng: np.random.Generator) -> list[np.ndarray]:
    intermediarios = np.arange(1, DESTINO)
    return [np.concatenate(([ORIGEM], rng.choice(intermediarios, NUM_INTERMEDIARIOS, replace=False), [DESTINO]))
            for _ in range(TAMANHO_POPULACAO)]


def selecao_torneio(populacao: list[np.ndarray], fitness: np.ndarray,
                    rng: np.random.Generator, tamanho: int = 3) -> np.ndarray:
    indices = rng.choice(len(populacao), tamanho, replace=False)
    return populacao[int(indices[np.argmin(fitness[indices])])]


def crossover_intermediarios(pai1: np.ndarray, pai2: np.ndarray,
                             rng: np.random.Generator) -> np.ndarray:
    """Crossover uniforme que mantém intermediários distintos."""
    escolhidos: list[int] = []
    for a, b in zip(pai1[1:-1], pai2[1:-1]):
        candidato = int(a if rng.random() < 0.5 else b)
        if candidato not in escolhidos:
            escolhidos.append(candidato)
    for candidato in rng.permutation(np.arange(1, DESTINO)):
        if len(escolhidos) == NUM_INTERMEDIARIOS:
            break
        if int(candidato) not in escolhidos:
            escolhidos.append(int(candidato))
    return np.array([ORIGEM, *escolhidos, DESTINO], dtype=int)


def mutacao(rota: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    filho = rota.copy()
    if rng.random() < TAXA_MUTACAO:
        i, j = rng.choice(np.arange(1, len(filho) - 1), 2, replace=False)
        filho[i], filho[j] = filho[j], filho[i]
    if rng.random() < TAXA_MUTACAO:
        usados = set(map(int, filho))
        disponiveis = [no for no in range(1, DESTINO) if no not in usados]
        if disponiveis:
            i = int(rng.integers(1, len(filho) - 1))
            filho[i] = int(rng.choice(disponiveis))
    return filho


def otimizar(topologia: Topologia | None = None, semente: int = SEMENTE) -> Resultado:
    topologia = topologia or criar_topologia(semente)
    rng = np.random.default_rng(semente + 1)
    populacao = criar_populacao(rng)
    historico: list[float] = []
    melhor = populacao[0].copy()
    melhor_fitness = float("inf")

    for _ in range(NUM_GERACOES):
        fitness = np.array([calcular_fitness(ind, topologia) for ind in populacao])
        indice = int(np.argmin(fitness))
        if fitness[indice] < melhor_fitness:
            melhor = populacao[indice].copy()
            melhor_fitness = float(fitness[indice])
        historico.append(melhor_fitness)
        nova = [melhor.copy()]
        while len(nova) < TAMANHO_POPULACAO:
            p1 = selecao_torneio(populacao, fitness, rng)
            p2 = selecao_torneio(populacao, fitness, rng)
            nova.append(mutacao(crossover_intermediarios(p1, p2, rng), rng))
        populacao = nova

    latencia, perda = calcular_metricas(melhor, topologia)
    inseguros = [int(no) for no in melhor if topologia.reputacao[int(no)] < LIMIAR_REPUTACAO]
    penalidade = PENALIDADE_SEGURANCA if inseguros else 0.0
    return Resultado(melhor, latencia, perda, penalidade, calcular_fitness(melhor, topologia), inseguros, historico)


def main() -> None:
    topologia = criar_topologia()
    resultado = otimizar(topologia)
    confiaveis = [int(no) for no, rep in enumerate(topologia.reputacao) if rep >= LIMIAR_REPUTACAO]
    print("=" * 72)
    print("DESAFIO AC-1 — MOTOR DE DECISIONING SD-WAN ZERO-TRUST")
    print("=" * 72)
    print(f"Rota selecionada: {' -> '.join(map(str, resultado.rota))}")
    print(f"Latência total: {resultado.latencia_total:.2f} ms")
    print(f"Perda acumulada: {resultado.perda_total:.2f} %")
    print(f"Nós confiáveis disponíveis: {confiaveis}")
    print(f"Nós não confiáveis na rota: {resultado.nos_nao_confiaveis or 'nenhum'}")
    print(f"Penalidade de segurança: {resultado.penalidade_seguranca:.2f}")
    print(f"Fitness final: {resultado.fitness:.2f}")
    print("Justificativa: rotas com qualquer reputação inferior a 50 recebem 5.000 pontos de multa;")
    print("a seleção, portanto, prioriza o menor custo ponderado entre as rotas sem risco de segurança.")


if __name__ == "__main__":
    main()


__all__ = ["Topologia", "Resultado", "criar_topologia", "calcular_metricas", "calcular_fitness", "otimizar"]

