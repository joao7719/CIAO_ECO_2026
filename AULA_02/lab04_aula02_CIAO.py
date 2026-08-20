"""Atividade 4 - Modelagem de selecao de disciplinas."""
import random
from itertools import product

DISCIPLINAS = [
    {"nome": "Algoritmos", "creditos": 4, "utilidade": 10, "pre_requisitos": []},
    {"nome": "Inteligencia Computacional", "creditos": 4, "utilidade": 10, "pre_requisitos": ["Algoritmos"]},
    {"nome": "Banco de Dados", "creditos": 4, "utilidade": 8, "pre_requisitos": []},
    {"nome": "Engenharia de Software", "creditos": 4, "utilidade": 7, "pre_requisitos": []},
    {"nome": "Computacao em Nuvem", "creditos": 2, "utilidade": 6, "pre_requisitos": ["Banco de Dados"]},
    {"nome": "Projeto Integrador", "creditos": 2, "utilidade": 5, "pre_requisitos": ["Algoritmos", "Engenharia de Software"]},
]
LIMITE_CREDITOS = 12


def avaliar_solucao(solucao):
    selecionadas = [d for d, escolhido in zip(DISCIPLINAS, solucao) if escolhido]
    nomes = {d["nome"] for d in selecionadas}
    creditos = sum(d["creditos"] for d in selecionadas)
    utilidade = sum(d["utilidade"] for d in selecionadas)
    sem_excesso = creditos <= LIMITE_CREDITOS
    prerequisitos_ok = all(set(d["pre_requisitos"]).issubset(nomes) for d in selecionadas)
    return {"creditos": creditos, "utilidade": utilidade, "factivel": sem_excesso and prerequisitos_ok,
            "selecionadas": [d["nome"] for d in selecionadas]}


def gerar_solucao_aleatoria(seed=42):
    random.seed(seed)
    while True:
        solucao = [random.randint(0, 1) for _ in DISCIPLINAS]
        avaliacao = avaliar_solucao(solucao)
        if avaliacao["factivel"]:
            return solucao, avaliacao


def contar_solucoes():
    return 2 ** len(DISCIPLINAS)


if __name__ == "__main__":
    solucao, avaliacao = gerar_solucao_aleatoria()
    print("PROBLEMA: selecao de disciplinas para o proximo semestre")
    print("Solucao aleatoria (0=nao cursa, 1=cursa):", solucao)
    print("Disciplinas:", ", ".join(avaliacao["selecionadas"]))
    print("Creditos totais:", avaliacao["creditos"])
    print("Utilidade total:", avaliacao["utilidade"])
    print("Solucao factivel:", avaliacao["factivel"])
    print("Espaco de busca:", contar_solucoes(), "solucoes")
