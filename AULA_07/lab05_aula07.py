"""LAB 05 — Busca local hill climbing em um algoritmo memético."""
import numpy as np

np.random.seed(42)

def rastrigin(x):
    return 10 * len(x) + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x))


def local_search_hill_climbing(solution, step_size=0.01, max_steps=20):
    current_sol = np.copy(solution)
    current_fit = rastrigin(current_sol)
    for _ in range(max_steps):
        neighbor = current_sol + np.random.uniform(-step_size, step_size, size=len(solution))
        neighbor_fit = rastrigin(neighbor)
        if neighbor_fit < current_fit:
            current_sol, current_fit = neighbor, neighbor_fit
    return current_sol, current_fit


initial_solution = np.array([2.5, -3.1])
refined_solution, final_fit = local_search_hill_climbing(initial_solution)
print(f"[LAB 05 - SUCESSO] Solução Inicial: {initial_solution} | Fitness: {rastrigin(initial_solution):.4f}")
print(f"[LAB 05] Solução Refinada: {refined_solution} | Fitness: {final_fit:.4f}")
