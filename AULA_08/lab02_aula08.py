"""Aula 08 / Lab 02 — AG binário para seleção de microsserviços em Edge.

Como o roteiro não fornece uma tabela de serviços, os 15 valores abaixo são
hipóteses didáticas declaradas e reproduzíveis. Dependências: numpy, matplotlib.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NOMES = ["Auth", "API", "Cache", "Busca", "Pagamentos", "Catálogo", "Fila", "Métricas", "Recomendação", "Imagens", "Notificações", "Perfil", "Relatórios", "Auditoria", "Recomendador ML"]
VALOR = np.array([18, 16, 14, 13, 20, 12, 11, 8, 15, 10, 9, 12, 7, 10, 19], dtype=float)
RAM = np.array([2.5, 2.0, 3.0, 1.5, 2.5, 2.0, 1.0, 1.0, 2.5, 2.0, 1.0, 1.5, 1.5, 1.0, 4.0])
CPU = np.array([1.2, 1.0, 0.8, 0.8, 1.5, 0.7, 0.6, 0.5, 1.3, 0.8, 0.5, 0.7, 0.6, 0.6, 2.0])
MAX_RAM, MAX_CPU = 16.0, 8.0
OUT = Path(__file__).resolve().parent


def avaliar(pop, estrategia):
    valor = pop @ VALOR
    ram = pop @ RAM
    cpu = pop @ CPU
    er = np.maximum(ram - MAX_RAM, 0.0)
    ec = np.maximum(cpu - MAX_CPU, 0.0)
    viavel = (er <= 1e-12) & (ec <= 1e-12)
    if estrategia == "rigida":
        fit = np.where(viavel, valor, 0.0)
    else:
        # Desconto linear, proporcional ao percentual excedente em cada recurso.
        fator = np.maximum(0.0, 1.0 - er / MAX_RAM - ec / MAX_CPU)
        fit = valor * fator
    return fit, valor, ram, cpu, viavel


def torneio(pop, fit, rng, k=3):
    candidatos = rng.integers(0, len(pop), size=(len(pop), k))
    vencedores = candidatos[np.arange(len(pop)), np.argmax(fit[candidatos], axis=1)]
    return pop[vencedores].copy()


def diversidade(pop):
    # Entropia binária média por locus; faixa [0,1].
    p = pop.mean(axis=0)
    h = -(np.where(p > 0, p*np.log2(np.maximum(p, 1e-12)), 0) + np.where(p < 1, (1-p)*np.log2(np.maximum(1-p, 1e-12)), 0))
    return float(h.mean())


def executar(estrategia, seed, populacao=120, geracoes=180):
    rng = np.random.default_rng(seed)
    pop = rng.integers(0, 2, size=(populacao, len(NOMES)), dtype=np.int8)
    medias, desvios, diversidades = [], [], []
    melhor_viavel_valor, melhor_viavel = -1.0, None
    melhor_fit_global, melhor_global = -1.0, None
    for _ in range(geracoes):
        fit, valor, _, _, viavel = avaliar(pop, estrategia)
        medias.append(float(fit.mean())); desvios.append(float(fit.std())); diversidades.append(diversidade(pop))
        if np.any(viavel):
            j = np.flatnonzero(viavel)[np.argmax(valor[viavel])]
            if valor[j] > melhor_viavel_valor:
                melhor_viavel_valor, melhor_viavel = float(valor[j]), pop[j].copy()
        j = int(np.argmax(fit))
        if fit[j] > melhor_fit_global:
            melhor_fit_global, melhor_global = float(fit[j]), pop[j].copy()
        pais = torneio(pop, fit, rng)
        filhos = pais.copy()
        ordem = rng.permutation(populacao)
        for a, b in zip(ordem[::2], ordem[1::2]):
            if rng.random() < 0.85:
                corte = int(rng.integers(1, len(NOMES)))
                filhos[a, corte:], filhos[b, corte:] = pais[b, corte:].copy(), pais[a, corte:].copy()
        mascara = rng.random(filhos.shape) < (1.0 / len(NOMES))
        filhos ^= mascara.astype(np.int8)
        # Elitismo preserva o melhor indivíduo da geração sem ocultar a diversidade.
        elite = pop[int(np.argmax(fit))].copy()
        pop = filhos
        fit_novo = avaliar(pop, estrategia)[0]
        pop[int(np.argmin(fit_novo))] = elite
    return np.array(medias), np.array(desvios), np.array(diversidades), melhor_viavel, melhor_viavel_valor, melhor_global


def brute_force():
    allp = ((np.arange(1 << len(NOMES))[:, None] >> np.arange(len(NOMES))) & 1).astype(np.int8)
    _, valor, _, _, ok = avaliar(allp, "rigida")
    i = np.flatnonzero(ok)[np.argmax(valor[ok])]
    return allp[i], float(valor[i])


def main():
    geracoes, execucoes = 180, 12
    agregado = {}
    for estrategia in ("rigida", "proporcional"):
        runs = [executar(estrategia, 811 + i, geracoes=geracoes) for i in range(execucoes)]
        agregado[estrategia] = runs
        encontrados = [(r[4], r[3]) for r in runs if r[3] is not None]
        melhor = max(encontrados, key=lambda z: z[0])
        print(f"{estrategia}: melhor_valor_viavel={melhor[0]:.1f}; genótipo={''.join(map(str, melhor[1].tolist()))}; diversidade_final_média={np.mean([r[2][-1] for r in runs]):.3f}; média_fitness_final={np.mean([r[0][-1] for r in runs]):.3f}; desvio_fitness_final={np.mean([r[1][-1] for r in runs]):.3f}")
    opt, optv = brute_force()
    print(f"ótimo exato por enumeração: valor={optv:.1f}; serviços={[NOMES[i] for i in np.flatnonzero(opt)]}")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    colors = {"rigida":"#2474B5", "proporcional":"#E07A25"}
    for estrategia, runs in agregado.items():
        mat = np.array([r[0] for r in runs]); means=mat.mean(axis=0); sd=mat.std(axis=0)
        axes[0].plot(means, label=estrategia.title(), color=colors[estrategia]); axes[0].fill_between(np.arange(geracoes), means-sd, means+sd, color=colors[estrategia], alpha=.16)
        axes[1].plot(np.mean([r[2] for r in runs], axis=0), label=estrategia.title(), color=colors[estrategia])
    axes[0].set(title="Fitness médio por geração (12 sementes)", xlabel="Geração", ylabel="Fitness"); axes[1].set(title="Diversidade genética (entropia média)", xlabel="Geração", ylabel="Entropia normalizada")
    for ax in axes: ax.grid(alpha=.25); ax.legend()
    fig.tight_layout(); fig.savefig(OUT/"comparacao_lab02_aula08.png", dpi=160)
    assert opt @ RAM <= MAX_RAM + 1e-9 and opt @ CPU <= MAX_CPU + 1e-9
    print("[OK] comparação concluída; solução de referência viável validada; gráfico salvo.")

if __name__ == "__main__": main()
