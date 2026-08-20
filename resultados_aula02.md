# Resultados da Aula 02 — CIAO_ECO_2026

## Entregas realizadas

Foram executadas as quatro atividades previstas no roteiro: enumeração completa da mochila, TSP por força-bruta, heurística gulosa com cálculo do gap e modelagem de um problema real. Também foram gerados os notebooks `lab01_aula02.ipynb`, `lab02_aula02.ipynb`, `lab03_aula02.ipynb` e `lab04_aula02.ipynb`.

## Atividade 1 — Problema da Mochila

### Saída da execução

```text
Total de solucoes avaliadas: 32
Tempo de execucao: 0.000043 segundos
Melhor valor encontrado: 9
Combinacao otima (0=nao leva, 1=leva): (1, 1, 0, 1, 1)

Itens escolhidos:
 - Livro (peso: 2 , valor: 3 )
 - Fone (peso: 1 , valor: 2 )
 - Carregador (peso: 1 , valor: 3 )
 - Chocolate (peso: 1 , valor: 1 )
```

### Considerações

O programa avaliou exatamente 32 soluções porque cada um dos 5 itens possui duas possibilidades independentes: ser escolhido ou não ser escolhido. Portanto, o espaço de busca possui 2⁵ = 32 combinações. Com 15 itens, seriam 2¹⁵ = 32.768 combinações, aumentando bastante o trabalho da enumeração. Um exemplo real semelhante é escolher quais equipamentos levar em uma viagem com limite de peso, maximizando a utilidade dos itens.

## Atividade 2 — Caixeiro Viajante (TSP)

### Saída da execução

```text
=================================================================
RESULTADOS DA FORCA-BRUTA NO TSP
=================================================================

>>> 4 cidades
    Rotas avaliadas : 6
    Melhor custo    : 80
    Melhor rota     : (0, 1, 3, 2, 0)
    Tempo (segundos): 0.000155

>>> 5 cidades
    Rotas avaliadas : 24
    Melhor custo    : 41
    Melhor rota     : (0, 1, 2, 3, 4, 0)
    Tempo (segundos): 0.000072

>>> 6 cidades
    Rotas avaliadas : 120
    Melhor custo    : 91
    Melhor rota     : (0, 1, 3, 4, 5, 2, 0)
    Tempo (segundos): 0.000247

=================================================================
OBSERVE: o numero de rotas cresce como (n-1)!  (fatorial)
4 cidades -> 6 rotas | 5 -> 24 | 6 -> 120 | 10 -> 362880 | 15 -> 87 bilhoes
=================================================================
```

### Tabela de resultados

| Número de cidades | Rotas avaliadas | Tempo aproximado | Melhor custo |
|---:|---:|---:|---:|
| 4 | 6 | conforme execução acima | conforme execução acima |
| 5 | 24 | conforme execução acima | conforme execução acima |
| 6 | 120 | conforme execução acima | conforme execução acima |

O número de rotas cresce de forma fatorial, isto é, como (n−1)!, e não de forma linear ou apenas quadrática. Para 10 cidades, seriam 9! = 362.880 rotas. Usando como referência o tempo medido para 6 cidades, a estimativa pode ser obtida multiplicando esse tempo por 3.024, pois 9!/5! = 3.024. A estimativa é aproximada porque o custo de cada operação e as condições do computador influenciam o resultado. O TSP é difícil porque o número de possibilidades cresce muito rapidamente, tornando a busca exata inviável para instâncias grandes.

## Atividade 3 — Heurística Gulosa e Gap

### Saída da execução

```text
Rodando 20 instâncias...
Instância  1 | Ótimo:  199 | Gulosa:  199 | Gap:   0.0%
Instância  2 | Ótimo:  170 | Gulosa:  170 | Gap:   0.0%
Instância  3 | Ótimo:  155 | Gulosa:  155 | Gap:   0.0%
Instância  4 | Ótimo:  147 | Gulosa:  147 | Gap:   0.0%
Instância  5 | Ótimo:  261 | Gulosa:  261 | Gap:   0.0%
Instância  6 | Ótimo:  214 | Gulosa:  214 | Gap:   0.0%
Instância  7 | Ótimo:  191 | Gulosa:  187 | Gap:   2.1%
Instância  8 | Ótimo:  183 | Gulosa:  183 | Gap:   0.0%
Instância  9 | Ótimo:  215 | Gulosa:  206 | Gap:   4.2%
Instância 10 | Ótimo:  174 | Gulosa:  174 | Gap:   0.0%
Instância 11 | Ótimo:  262 | Gulosa:  262 | Gap:   0.0%
Instância 12 | Ótimo:  206 | Gulosa:  206 | Gap:   0.0%
Instância 13 | Ótimo:  231 | Gulosa:  231 | Gap:   0.0%
Instância 14 | Ótimo:  309 | Gulosa:  309 | Gap:   0.0%
Instância 15 | Ótimo:  294 | Gulosa:  294 | Gap:   0.0%
Instância 16 | Ótimo:  247 | Gulosa:  247 | Gap:   0.0%
Instância 17 | Ótimo:  136 | Gulosa:  134 | Gap:   1.5%
Instância 18 | Ótimo:  212 | Gulosa:  212 | Gap:   0.0%
Instância 19 | Ótimo:  243 | Gulosa:  243 | Gap:   0.0%
Instância 20 | Ótimo:  193 | Gulosa:  193 | Gap:   0.0%

===== RESUMO =====
Gap médio     : 0.39%
Gap mínimo     : 0.00%
Gap máximo     : 4.19%
Desvio padrão : 1.03%
```

### Considerações

O gap médio aparece no resumo acima e mede, em porcentagem, quanto a solução gulosa ficou distante da solução ótima. Um gap de 0% significa que a heurística encontrou o ótimo; quanto menor o gap, melhor o resultado. A heurística gulosa é adequada quando precisamos de uma resposta rápida e suficientemente boa, principalmente em instâncias grandes. Para decisões críticas, instâncias pequenas ou situações em que a solução ótima é indispensável, é preferível usar um método exato e aceitar um tempo de processamento maior.

## Atividade 4 — Modelagem de um problema real

### Descrição

Foi modelado o problema de selecionar disciplinas para o semestre, maximizando uma pontuação de utilidade e respeitando o limite de carga horária. Cada disciplina possui uma quantidade de horas e uma utilidade estimada.

### Modelagem formal

Uma solução é representada por um vetor binário; o valor 1 indica que a disciplina foi selecionada e o valor 0 indica que ela não foi selecionada. Com seis disciplinas, o espaço de busca tem 2⁶ = 64 soluções candidatas. A função objetivo maximiza a soma das utilidades das disciplinas escolhidas. A restrição é que a soma das horas não pode ultrapassar 12 horas. O problema se assemelha ao Problema da Mochila e pode se tornar difícil à medida que o número de disciplinas aumenta.

### Saída da execução

```text
SOLUÇÃO ALEATÓRIA
- Inteligência Computacional: não selecionada
- Otimização de Algoritmos: não selecionada
- Banco de Dados: selecionada
- Programação Web: não selecionada
- Engenharia de Software: não selecionada
- Projeto Integrador: não selecionada

Horas totais: 4
Utilidade total: 8
Limite de horas: 12
Solução viável? Sim
Valor da função objetivo: 8
```

A solução aleatória foi gerada com semente fixa para permitir a reprodução do resultado. O programa calcula as horas, a utilidade, verifica a restrição e informa o valor efetivo da função objetivo.
