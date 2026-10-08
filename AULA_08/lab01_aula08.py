"""Aula 08 / Lab 01 — PSO contínuo para balanceamento térmico em 6 AZs.

Modelo explícito: T_i = 25 + C_i * (6*w_i)^2 (°C). O fator 6 normaliza a
carga relativa em relação à distribuição uniforme; o termo quadrático modela
congestionamento térmico. A função objetivo é a média ponderada das temperaturas
mais penalidade externa quando alguma AZ supera 75 °C.
Dependências: numpy, matplotlib.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C = np.array([42.0, 35.0, 58.0, 30.0, 50.0, 65.0])
AMBIENTE = 25.0
LIMITE = 75.0
PENALIDADE = 100.0
SEED = 20261007
OUT = Path(__file__).resolve().parent


def normalizar(p):
    """Projeta cada vetor de posição no simplex não negativo sum(w)=1."""
    p = np.maximum(np.asarray(p, dtype=float), 1e-12)
    return p / p.sum(axis=-1, keepdims=True)


def temperaturas(w):
    return AMBIENTE + C * (6.0 * np.asarray(w)) ** 2


def fitness(w):
    t = temperaturas(w)
    media_ponderada = float(np.dot(w, t))
    excesso = np.maximum(0.0, t - LIMITE)
    return media_ponderada + PENALIDADE * float(np.dot(excesso, excesso))


def pso(n_particulas, n_iter=300, seed=SEED):
    rng = np.random.default_rng(seed + n_particulas)
    x = normalizar(rng.random((n_particulas, 6)))
    v = rng.normal(0.0, 0.04, size=x.shape)
    pbest = x.copy()
    pfit = np.array([fitness(z) for z in x])
    idx = int(np.argmin(pfit))
    gbest, gfit = pbest[idx].copy(), float(pfit[idx])
    historico = []
    w_inercia, c1, c2 = 0.68, 1.45, 1.45
    for _ in range(n_iter):
        r1, r2 = rng.random(x.shape), rng.random(x.shape)
        v = w_inercia * v + c1 * r1 * (pbest - x) + c2 * r2 * (gbest - x)
        v = np.clip(v, -0.25, 0.25)
        x = normalizar(x + v)
        vals = np.array([fitness(z) for z in x])
        improved = vals < pfit
        pbest[improved], pfit[improved] = x[improved], vals[improved]
        j = int(np.argmin(pfit))
        if pfit[j] < gfit:
            gbest, gfit = pbest[j].copy(), float(pfit[j])
        historico.append(gfit)
    return gbest, gfit, np.asarray(historico)


def main():
    resultados = {}
    plt.figure(figsize=(9, 5.2))
    for n in (10, 30, 50):
        w, f, hist = pso(n)
        resultados[n] = (w, f)
        plt.semilogy(hist, label=f"{n} partículas")
        temps = temperaturas(w)
        print(f"população={n} | fitness={f:.6f} | W={np.array2string(w, precision=5)} | soma={w.sum():.12f} | Tmax={temps.max():.3f} °C")
    plt.title("PSO — convergência do melhor fitness")
    plt.xlabel("Iteração"); plt.ylabel("Fitness (escala log; °C + penalidade)")
    plt.grid(alpha=.25); plt.legend(); plt.tight_layout()
    plt.savefig(OUT / "convergencia_lab01_aula08.png", dpi=160)
    # Validações do melhor resultado de cada população.
    for w, _ in resultados.values():
        assert np.isclose(w.sum(), 1.0, atol=1e-10) and np.all(w >= 0)
        assert np.max(temperaturas(w)) <= LIMITE + 1e-2
    print("[OK] normalização e limite térmico validados; gráfico salvo.")

if __name__ == "__main__":
    main()
