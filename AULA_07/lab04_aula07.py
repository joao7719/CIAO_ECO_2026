"""LAB 04 — Atualização de feromônio em ACO."""
import numpy as np

latency_matrix = np.array([
    [0, 5, 2, 9],
    [5, 0, 3, 1],
    [2, 3, 0, 7],
    [9, 1, 7, 0],
], dtype=float)
pheromone = np.ones((len(latency_matrix), len(latency_matrix)), dtype=float)
rho = 0.25


def update_pheromone(pheromone_matrix, paths, costs, rho):
    updated = pheromone_matrix * (1 - rho)
    for path, cost in zip(paths, costs):
        if cost <= 0:
            raise ValueError("O custo deve ser positivo.")
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            updated[u, v] += 1.0 / cost
    return updated


mock_paths = [[0, 2, 1, 3], [0, 1, 3]]
mock_costs = [6.0, 6.0]
updated_pheromone = update_pheromone(pheromone, mock_paths, mock_costs, rho)
print("[LAB 04 - SUCESSO] Matriz de Feromônio Atualizada:\n", updated_pheromone)
