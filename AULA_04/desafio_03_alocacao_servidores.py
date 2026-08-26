"""
Desafio 03 — Balanceamento de carga em servidores.

Um indivíduo é um vetor de 20 posições. O índice representa uma tarefa e o
valor em [0, 3] representa o servidor que executará essa tarefa. O algoritmo
genético minimiza o makespan, isto é, a maior carga acumulada entre os quatro
servidores.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

TEMPOS = np.array([12, 35, 40, 8, 15, 22, 19, 45, 60, 31,
                   14, 28, 50, 18, 25, 33, 42, 10, 5, 29], dtype=float)
NUM_SERVIDORES = 4
TAMANHO_POPULACAO = 80
NUM_GERACOES = 250
TAXA_MUTACAO = 0.12
SEMENTE = 2026


@dataclass(frozen=True)
class Resultado:
    alocacao: np.ndarray
    cargas: np.ndarray
    makespan: float
    historico: list[float]


def calcular_cargas(alocacao: np.ndarray, tempos: np.ndarray = TEMPOS,
                    num_servidores: int = NUM_SERVIDORES) -> np.ndarray:
    """Retorna a carga total de cada servidor."""
    cargas = np.zeros(num_servidores, dtype=float)
    for tarefa, servidor in enumerate(alocacao):
        if not 0 <= int(servidor) < num_servidores:
            raise ValueError("Toda tarefa deve ser atribuída a um servidor em [0, 3].")
        cargas[int(servidor)] += tempos[tarefa]
    return cargas


def calcular_makespan(alocacao: np.ndarray, tempos: np.ndarray = TEMPOS) -> float:
    """Calcula o tempo do servidor mais carregado."""
    return float(np.max(calcular_cargas(alocacao, tempos)))


def criar_populacao(rng: np.random.Generator, tamanho: int) -> list[np.ndarray]:
    return [rng.integers(0, NUM_SERVIDORES, size=len(TEMPOS), dtype=int)
            for _ in range(tamanho)]


def selecao_torneio(populacao: list[np.ndarray], fitness: np.ndarray,
                    rng: np.random.Generator, tamanho: int = 3) -> np.ndarray:
    indices = rng.choice(len(populacao), size=tamanho, replace=False)
    vencedor = indices[np.argmin(fitness[indices])]
    return populacao[int(vencedor)]


def crossover_uniforme(pai1: np.ndarray, pai2: np.ndarray,
                       rng: np.random.Generator) -> np.ndarray:
    mascara = rng.random(len(pai1)) < 0.5
    return np.where(mascara, pai1, pai2).astype(int)


def mutacao_realocacao(individuo: np.ndarray, rng: np.random.Generator,
                        taxa: float = TAXA_MUTACAO) -> np.ndarray:
    filho = individuo.copy()
    for i in range(len(filho)):
        if rng.random() < taxa:
            filho[i] = rng.integers(0, NUM_SERVIDORES)
    return filho


def otimizar(semente: int = SEMENTE) -> Resultado:
    rng = np.random.default_rng(semente)
    populacao = criar_populacao(rng, TAMANHO_POPULACAO)
    historico: list[float] = []
    melhor = populacao[0].copy()
    melhor_fitness = float("inf")

    for _ in range(NUM_GERACOES):
        fitness = np.array([calcular_makespan(ind) for ind in populacao])
        indice = int(np.argmin(fitness))
        if fitness[indice] < melhor_fitness:
            melhor = populacao[indice].copy()
            melhor_fitness = float(fitness[indice])
        historico.append(melhor_fitness)

        nova_populacao = [melhor.copy()]  # elitismo
        while len(nova_populacao) < TAMANHO_POPULACAO:
            pai1 = selecao_torneio(populacao, fitness, rng)
            pai2 = selecao_torneio(populacao, fitness, rng)
            filho = crossover_uniforme(pai1, pai2, rng)
            nova_populacao.append(mutacao_realocacao(filho, rng))
        populacao = nova_populacao

    cargas = calcular_cargas(melhor)
    return Resultado(melhor, cargas, float(np.max(cargas)), historico)


def main() -> None:
    resultado = otimizar()
    print("=" * 64)
    print("DESAFIO 03 — BALANCEAMENTO DE CARGA")
    print("=" * 64)
    print(f"Alocação tarefa -> servidor: {resultado.alocacao.tolist()}")
    print(f"Cargas por servidor (s): {resultado.cargas.tolist()}")
    print(f"Makespan mínimo encontrado (s): {resultado.makespan:.2f}")
    print(f"Desbalanceamento máximo (s): {resultado.cargas.max() - resultado.cargas.min():.2f}")
    print("A solução utiliza elitismo, seleção por torneio, crossover uniforme e mutação por realocação.")


if __name__ == "__main__":
    main()


__all__ = ["TEMPOS", "calcular_cargas", "calcular_makespan", "otimizar", "Resultado"]


# Nota: a soma dos tempos é 541 s; portanto, o limite teórico inferior do
# makespan é ceil(541 / 4) = 136 s. O algoritmo busca uma alocação próxima
# desse limite sem violar a representação pedida no enunciado.

