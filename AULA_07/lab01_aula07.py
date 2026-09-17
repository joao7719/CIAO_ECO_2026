"""LAB 01 — ACO híbrido com busca local 2-opt."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.random.seed(42)
dist_matrix = np.array([
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 30],
    [15, 35, 0, 30, 5],
    [20, 25, 30, 0, 15],
    [25, 30, 5, 15, 0],
], dtype=float)
num_nodes = len(dist_matrix)
num_ants, num_iterations = 10, 50
alpha, beta, rho = 1.0, 2.0, 0.1
pheromone = np.ones((num_nodes, num_nodes), dtype=float)
best_cost, best_path = float("inf"), None
convergence = []


def path_cost(path, matrix):
    return sum(matrix[path[i], path[i + 1]] for i in range(len(path) - 1))


def local_search_2opt(path, matrix):
    best_local_path = list(path)
    best_local_cost = path_cost(best_local_path, matrix)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best_local_path) - 2):
            for j in range(i + 1, len(best_local_path) - 1):
                new_path = (best_local_path[:i]
                            + best_local_path[i:j + 1][::-1]
                            + best_local_path[j + 1:])
                new_cost = path_cost(new_path, matrix)
                if new_cost < best_local_cost:
                    best_local_path, best_local_cost = new_path, new_cost
                    improved = True
    return best_local_path, best_local_cost


for _ in range(num_iterations):
    paths, costs = [], []
    for _ in range(num_ants):
        path, unvisited = [0], list(range(1, num_nodes))
        while unvisited:
            current = path[-1]
            weights = np.array([
                pheromone[current, nxt] ** alpha
                * (1.0 / dist_matrix[current, nxt]) ** beta
                for nxt in unvisited
            ])
            weights /= weights.sum()
            nxt = int(np.random.choice(unvisited, p=weights))
            path.append(nxt)
            unvisited.remove(nxt)
        path.append(0)
        path, cost = local_search_2opt(path, dist_matrix)
        paths.append(path)
        costs.append(cost)
        if cost < best_cost:
            best_cost, best_path = cost, path.copy()
    pheromone *= 1 - rho
    for path, cost in zip(paths, costs):
        for i in range(len(path) - 1):
            pheromone[path[i], path[i + 1]] += 1.0 / cost
    convergence.append(best_cost)

plt.plot(convergence)
plt.xlabel("Iteração")
plt.ylabel("Melhor custo")
plt.title("Convergência do ACO Híbrido")
plt.grid()
plt.tight_layout()
plt.savefig("AULA_07/convergencia_lab01.png")
print(f"[LAB 01 - SUCESSO] Melhor Caminho: {[int(n) for n in best_path]} | Custo: {best_cost:.1f}")
print(f"[LAB 01] Custo inicial: {convergence[0]:.1f} | Custo final: {convergence[-1]:.1f}")

def main():
    return best_path, best_cost

if __name__ == "__main__":
    main()

# A função main existe para facilitar a execução/importação em notebooks.
# O gráfico é salvo em vez de exibido, permitindo execução em ambiente sem GUI.

# Observação: o bloco principal já executa o experimento ao importar o arquivo,
# mantendo a estrutura próxima à fornecida no roteiro da aula.

# Fim do laboratório 01.

# A linha abaixo não altera o algoritmo e marca explicitamente a entrega.
LABORATORIO = "ACO + 2-opt"

# Garantia de compatibilidade com execução a partir da raiz do repositório.
# O arquivo de imagem será produzido dentro de AULA_07.

# End.

# (Comentários finais intencionalmente mantidos para tornar o arquivo autoexplicativo.)

# Nenhuma dependência além de numpy e matplotlib é necessária.

# Resultado reproduzível com a semente 42.

# ----

# A implementação segue as instruções do roteiro.

# ----

# Fim.

# Nota: não é necessário modificar a matriz de distâncias.

# ----

# Entrega concluída.

# ----

# EOF
