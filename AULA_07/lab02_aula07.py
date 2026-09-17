"""LAB 02 — Algoritmo genético para o problema da mochila."""
import numpy as np

np.random.seed(42)
weights = np.array([12, 2, 1, 4, 1])
values = np.array([4, 2, 1, 10, 2])
max_weight = 15
pop_size, num_genes, generations = 10, len(weights), 10
mutation_rate = 0.1
population = np.random.randint(0, 2, size=(pop_size, num_genes))


def calculate_fitness(ind):
    total_weight = np.sum(ind * weights)
    total_value = np.sum(ind * values)
    return 0 if total_weight > max_weight else int(total_value)


def tournament_selection(pop, fitnesses):
    candidates = np.random.choice(len(pop), size=2, replace=False)
    winner = candidates[np.argmax(fitnesses[candidates])]
    return pop[winner].copy()


def crossover(parent1, parent2):
    point = np.random.randint(1, num_genes)
    return (np.concatenate([parent1[:point], parent2[point:]]),
            np.concatenate([parent2[:point], parent1[point:]]))


def mutate(ind):
    child = ind.copy()
    for i in range(num_genes):
        if np.random.rand() < mutation_rate:
            child[i] = 1 - child[i]
    return child


for generation in range(generations):
    fitnesses = np.array([calculate_fitness(ind) for ind in population])
    new_population = []
    for _ in range(pop_size // 2):
        p1 = tournament_selection(population, fitnesses)
        p2 = tournament_selection(population, fitnesses)
        c1, c2 = crossover(p1, p2)
        new_population.extend([mutate(c1), mutate(c2)])
    population = np.array(new_population)

fitnesses = np.array([calculate_fitness(ind) for ind in population])
best_index = int(np.argmax(fitnesses))
best = population[best_index]
print(f"[LAB 02 - SUCESSO] Melhor indivíduo: {best.tolist()}")
print(f"[LAB 02] Peso: {int(np.sum(best * weights))} | Valor: {int(fitnesses[best_index])}")
