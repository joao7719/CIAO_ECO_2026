# Atividade 4 — Modelagem de um problema real: seleção de disciplinas
# Objetivo: maximizar a utilidade das disciplinas sem ultrapassar a carga horária.
import random


disciplinas = [
    {'nome': 'Inteligência Computacional', 'horas': 4, 'utilidade': 10},
    {'nome': 'Otimização de Algoritmos', 'horas': 4, 'utilidade': 9},
    {'nome': 'Banco de Dados', 'horas': 4, 'utilidade': 8},
    {'nome': 'Programação Web', 'horas': 3, 'utilidade': 8},
    {'nome': 'Engenharia de Software', 'horas': 3, 'utilidade': 7},
    {'nome': 'Projeto Integrador', 'horas': 5, 'utilidade': 10},
]
limite_horas = 12

# Uma solução candidata é um vetor binário: 1 cursa a disciplina, 0 não cursa.
# A geração é aleatória, como solicitado no enunciado.
random.seed(42)
solucao = [random.randint(0, 1) for _ in disciplinas]

horas_total = sum(escolhida * disciplina['horas'] for escolhida, disciplina in zip(solucao, disciplinas))
utilidade_total = sum(escolhida * disciplina['utilidade'] for escolhida, disciplina in zip(solucao, disciplinas))
viavel = horas_total <= limite_horas

print('SOLUÇÃO ALEATÓRIA')
for escolhida, disciplina in zip(solucao, disciplinas):
    estado = 'selecionada' if escolhida else 'não selecionada'
    print(f"- {disciplina['nome']}: {estado}")
print(f'\nHoras totais: {horas_total}')
print(f'Utilidade total: {utilidade_total}')
print(f'Limite de horas: {limite_horas}')
print(f'Solução viável? {"Sim" if viavel else "Não"}')

# A função objetivo é maximizar a utilidade. Para uma solução inviável,
# o valor efetivo é considerado inválido, embora a utilidade bruta também seja exibida.
valor_objetivo = utilidade_total if viavel else float('-inf')
print(f'Valor da função objetivo: {valor_objetivo}')
