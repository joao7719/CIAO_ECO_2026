"""LAB 03 — Particle Swarm Optimization (PSO)."""
import numpy as np

np.random.seed(42)

def fitness_function(position):
    return np.sum(position ** 2)

num_particles, dimensions, max_iter = 10, 2, 15
X = np.random.uniform(-5, 5, (num_particles, dimensions))
V = np.random.uniform(-1, 1, (num_particles, dimensions))
pbest_X = np.copy(X)
pbest_fitness = np.array([fitness_function(p) for p in pbest_X])
gbest_X = np.copy(pbest_X[np.argmin(pbest_fitness)])
w, c1, c2 = 0.5, 1.5, 1.5

for _ in range(max_iter):
    for i in range(num_particles):
        r1, r2 = np.random.rand(), np.random.rand()
        V[i] = (w * V[i]) + (c1 * r1 * (pbest_X[i] - X[i])) + (c2 * r2 * (gbest_X - X[i]))
        X[i] = X[i] + V[i]
        current_fitness = fitness_function(X[i])
        if current_fitness < pbest_fitness[i]:
            pbest_fitness[i] = current_fitness
            pbest_X[i] = X[i].copy()
            if current_fitness < fitness_function(gbest_X):
                gbest_X = X[i].copy()

print(f"[LAB 03 - SUCESSO] Melhor posição encontrada pelo Enxame (gbest): {gbest_X}")
print(f"[LAB 03] Fitness do gbest: {fitness_function(gbest_X):.8f}")
