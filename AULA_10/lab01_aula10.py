"""AULA 10 — Motor de inferência Mamdani e superfície de decisão.

Dependências: python -m pip install numpy scipy matplotlib scikit-fuzzy
Execução:     python AULA_10/lab01_aula10.py

O programa compara centroide com conjuntos triangulares, centroide com
ombros trapezoidais nas bordas e MOM (Mean of Maximum) com triângulos.
Também valida a cobertura das entradas, imprime a matriz de regras e salva
AULA_10/superficie_decisao.png.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # permite executar em terminal sem interface gráfica
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# Universos de discurso: Impacto [0, 100], Explorabilidade [0, 10],
# Urgência [0, 100]. Resolução fina na saída reduz artefatos de discretização.
IMPACTO_UNIVERSE = np.arange(0, 101, 1, dtype=float)
EXPLORABILIDADE_UNIVERSE = np.arange(0, 10.01, 0.1, dtype=float)
URGENCIA_UNIVERSE = np.arange(0, 100.01, 0.25, dtype=float)

MATRIZ_REGRAS = (
    ("baixa", "baixa", "media"),
    ("media", "alta", "alta"),
    ("critica", "critica", "critica"),
)


def construir_sistema(metodo="centroid", trapezio_bordas=False):
    """Monta um sistema Mamdani completo; retorna variáveis e simulador."""
    impacto = ctrl.Antecedent(IMPACTO_UNIVERSE, "impacto")
    explorabilidade = ctrl.Antecedent(EXPLORABILIDADE_UNIVERSE, "explorabilidade")
    urgencia = ctrl.Consequent(
        URGENCIA_UNIVERSE, "urgencia", defuzzify_method=metodo
    )

    # Os conjuntos vizinhos se sobrepõem, sem lacunas em todo o domínio.
    impacto["baixo"] = fuzz.trapmf(impacto.universe, [0, 0, 20, 40])
    impacto["medio"] = fuzz.trimf(impacto.universe, [20, 50, 80])
    impacto["alto"] = fuzz.trapmf(impacto.universe, [60, 80, 100, 100])

    explorabilidade["baixa"] = fuzz.trapmf(
        explorabilidade.universe, [0, 0, 2, 4]
    )
    explorabilidade["moderada"] = fuzz.trimf(
        explorabilidade.universe, [2, 5, 8]
    )
    explorabilidade["alta"] = fuzz.trapmf(
        explorabilidade.universe, [6, 8, 10, 10]
    )

    if trapezio_bordas:
        # Ombros nas duas extremidades. O de urgência crítica é a Abordagem A.
        urgencia["baixa"] = fuzz.trapmf(
            urgencia.universe, [0, 0, 12, 32]
        )
        urgencia["critica"] = fuzz.trapmf(
            urgencia.universe, [65, 82, 100, 100]
        )
    else:
        # Conjuntos triangulares/triangulares de borda para a comparação MOM.
        urgencia["baixa"] = fuzz.trimf(urgencia.universe, [0, 0, 32])
        urgencia["critica"] = fuzz.trimf(
            urgencia.universe, [68, 100, 100]
        )
    urgencia["media"] = fuzz.trimf(urgencia.universe, [15, 40, 65])
    urgencia["alta"] = fuzz.trimf(urgencia.universe, [45, 70, 90])

    conjuntos_impacto = ("baixo", "medio", "alto")
    conjuntos_explorabilidade = ("baixa", "moderada", "alta")
    regras = []
    for i, nome_impacto in enumerate(conjuntos_impacto):
        for j, nome_explorabilidade in enumerate(conjuntos_explorabilidade):
            consequente = MATRIZ_REGRAS[i][j]
            regras.append(
                ctrl.Rule(
                    impacto[nome_impacto] & explorabilidade[nome_explorabilidade],
                    urgencia[consequente],
                    label=f"{nome_impacto}_{nome_explorabilidade}_para_{consequente}",
                )
            )

    sistema = ctrl.ControlSystem(regras)
    simulador = ctrl.ControlSystemSimulation(sistema, cache=False)
    return impacto, explorabilidade, urgencia, simulador


def calcular(simulador, impacto, explorabilidade):
    """Calcula uma saída escalar para um par de entradas validado."""
    if not 0 <= impacto <= 100:
        raise ValueError("Impacto deve estar no intervalo [0, 100].")
    if not 0 <= explorabilidade <= 10:
        raise ValueError("Explorabilidade deve estar no intervalo [0, 10].")
    simulador.input["impacto"] = float(impacto)
    simulador.input["explorabilidade"] = float(explorabilidade)
    simulador.compute()
    return float(simulador.output["urgencia"])


def validar_cobertura():
    """Falha cedo se algum conjunto de entrada deixar uma lacuna no universo."""
    impacto, explorabilidade, _, _ = construir_sistema()
    for variavel in (impacto, explorabilidade):
        cobertura = np.zeros_like(variavel.universe, dtype=float)
        for nome in variavel.terms:
            cobertura = np.maximum(cobertura, variavel[nome].mf)
        if np.any(cobertura <= 0):
            indices = np.flatnonzero(cobertura <= 0)
            raise RuntimeError(
                f"Lacuna de cobertura em {variavel.label}: "
                f"{variavel.universe[indices[:5]]}"
            )


def imprimir_matriz():
    """Exibe a matriz 3 x 3 solicitada no enunciado."""
    print("\nMatriz de regras (linhas: Impacto; colunas: Explorabilidade)")
    print(f"{'':<12} {'Baixa':<14} {'Moderada':<14} {'Alta':<14}")
    rótulos = ("Baixo", "Médio", "Alto")
    for rótulo, linha in zip(rótulos, MATRIZ_REGRAS):
        print(f"{rótulo:<12} {linha[0]:<14} {linha[1]:<14} {linha[2]:<14}")


def comparar_extremos():
    """Compara as configurações do desafio em (0,0) e (100,10)."""
    configurações = (
        ("Centroide + bordas triangulares", "centroid", False),
        ("Abordagem A: centroide + trapézios nas bordas", "centroid", True),
        ("Abordagem B: MOM + bordas triangulares", "mom", False),
    )
    resultados = {}
    print("\nComparação dos extremos (Impacto, Explorabilidade -> Urgência):")
    for nome, método, trapézios in configurações:
        _, _, _, sim = construir_sistema(método, trapézios)
        mínimo = calcular(sim, 0, 0)
        máximo = calcular(sim, 100, 10)
        meio = calcular(sim, 50, 5)
        resultados[nome] = (mínimo, máximo, meio)
        print(
            f"- {nome}: (0, 0) = {mínimo:.2f}%; "
            f"(100, 10) = {máximo:.2f}%; (50, 5) = {meio:.2f}%"
        )
    return resultados


def medir_suavidade():
    """Compara a maior variação ao alterar impacto em passos de 0,5 ponto."""
    entradas = np.linspace(0, 100, 201)
    configurações = (
        ("Centroide + trapézios", "centroid", True),
        ("MOM + triângulos", "mom", False),
    )
    print("\nSuavidade em explorabilidade = 5 (passo de impacto = 0,5):")
    for nome, método, trapézios in configurações:
        _, _, _, simulador = construir_sistema(método, trapézios)
        saídas = np.array([calcular(simulador, x, 5) for x in entradas])
        diferenças = np.abs(np.diff(saídas))
        print(
            f"- {nome}: maior variação adjacente = {diferenças.max():.2f} "
            f"pontos percentuais; variações > 1 p.p. = "
            f"{np.count_nonzero(diferenças > 1)}"
        )


def gerar_superficie(caminho):
    """Calcula e plota a superfície 3D usando centroide e bordas trapezoidais."""
    _, _, _, simulador = construir_sistema("centroid", trapezio_bordas=True)
    valores_impacto = np.linspace(0, 100, 51)
    valores_explorabilidade = np.linspace(0, 10, 26)
    grade_impacto, grade_explorabilidade = np.meshgrid(
        valores_impacto, valores_explorabilidade
    )
    grade_urgencia = np.empty_like(grade_impacto, dtype=float)

    for índice_y, explorabilidade in enumerate(valores_explorabilidade):
        for índice_x, impacto in enumerate(valores_impacto):
            grade_urgencia[índice_y, índice_x] = calcular(
                simulador, impacto, explorabilidade
            )

    fig = plt.figure(figsize=(12, 8), constrained_layout=True)
    ax = fig.add_subplot(111, projection="3d")
    superfície = ax.plot_surface(
        grade_impacto,
        grade_explorabilidade,
        grade_urgencia,
        cmap="viridis",
        edgecolor="none",
        antialiased=True,
        rstride=1,
        cstride=1,
    )
    ax.set_title("Superfície de decisão fuzzy — Sistema Mamdani", pad=18)
    ax.set_xlabel("Impacto (%)", labelpad=10)
    ax.set_ylabel("Explorabilidade (0–10)", labelpad=10)
    ax.set_zlabel("Urgência (%)", labelpad=10)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10)
    ax.set_zlim(0, 100)
    ax.view_init(elev=28, azim=-135)
    fig.colorbar(superfície, ax=ax, shrink=0.65, pad=0.1, label="Urgência (%)")
    caminho.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(caminho, dpi=180, bbox_inches="tight")
    plt.close(fig)

    print(
        f"\nSuperfície salva em: {caminho}\n"
        f"Faixa observada: {grade_urgencia.min():.2f}%–"
        f"{grade_urgencia.max():.2f}% em {grade_urgencia.size} pontos."
    )


def main():
    validar_cobertura()
    print("Cobertura das funções de pertinência: sem lacunas.")
    imprimir_matriz()
    comparar_extremos()
    medir_suavidade()
    arquivo_imagem = Path(__file__).resolve().with_name("superficie_decisao.png")
    gerar_superficie(arquivo_imagem)


if __name__ == "__main__":
    main()
