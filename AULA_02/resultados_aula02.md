# Resultados e considerações — Aula 2

Este arquivo reúne as execuções dos quatro laboratórios da Aula 2. Os tempos podem variar ligeiramente conforme o computador, mas as quantidades de soluções e os custos ótimos são determinísticos.

## Atividade 1 — Enumeração completa da mochila

### Resultado da execução

```text
Total de solucoes avaliadas: 32
Tempo de execucao: 0.000030 segundos
Melhor valor encontrado: 9
Combinacao otima (0=nao leva, 1=leva): (1, 1, 0, 1, 1)

Itens escolhidos:
 - Livro (peso: 2 , valor: 3 )
 - Fone (peso: 1 , valor: 2 )
 - Carregador (peso: 1 , valor: 3 )
 - Chocolate (peso: 1 , valor: 1 )
```

A enumeração avaliou exatamente **32 soluções**, pois cada um dos cinco itens possui duas possibilidades: ser escolhido ou não ser escolhido. Assim, o espaço de busca é `2^5 = 32`. A melhor combinação encontrada tem valor 9 e respeita a capacidade de peso 5. Se o problema tivesse 15 itens, seriam `2^15 = 32.768` combinações; com o crescimento dos itens, a enumeração completa rapidamente se torna pouco prática.

Um problema cotidiano semelhante é montar uma lista de compras com orçamento limitado, escolhendo produtos que tragam maior utilidade sem ultrapassar o orçamento disponível.

## Atividade 2 — Caixeiro Viajante por força-bruta

### Resultado da execução

```text
=================================================================
RESULTADOS DA FORCA-BRUTA NO TSP
=================================================================

>>> 4 cidades
    Rotas avaliadas : 6
    Melhor custo    : 80
    Melhor rota     : (0, 1, 3, 2, 0)
    Tempo (segundos): 0.000049

>>> 5 cidades
    Rotas avaliadas : 24
    Melhor custo    : 41
    Melhor rota     : (0, 1, 2, 3, 4, 0)
    Tempo (segundos): 0.000039

>>> 6 cidades
    Rotas avaliadas : 120
    Melhor custo    : 91
    Melhor rota     : (0, 1, 3, 4, 5, 2, 0)
    Tempo (segundos): 0.000176

=================================================================
OBSERVE: o numero de rotas cresce como (n-1)!  (fatorial)
4 cidades -> 6 rotas | 5 -> 24 | 6 -> 120 | 10 -> 362880 | 15 -> 87 bilhoes
=================================================================
```

| Cidades | Rotas avaliadas | Melhor custo |
|---:|---:|---:|
| 4 | 6 | 80 |
| 5 | 24 | 41 |
| 6 | 120 | 91 |

A quantidade de rotas cresce de forma fatorial, pois o algoritmo avalia `(n-1)!` permutações. Isso é muito mais rápido do que um crescimento linear ou quadrático. Para 10 cidades, seriam 362.880 rotas; usando como referência o tempo observado para 6 cidades, a estimativa é obtida multiplicando o tempo por `362.880 / 120 = 3.024`, embora a medição real dependa do hardware e da implementação. Para 15 cidades, seriam 87.178.291.200 rotas, tornando a força-bruta inviável.

O TSP é considerado difícil porque o número de possibilidades cresce muito rapidamente com o número de cidades. Em instâncias pequenas, o método exato garante a melhor rota; em instâncias maiores, heurísticas e metaheurísticas são alternativas mais adequadas.

## Atividade 3 — Heurística gulosa e gap de otimalidade

### Resultado da execução

```text
Rodando 20 instancias...
Instancia  1 | Otimo:  199 | Gulosa:  199 | Gap:   0.0%
Instancia  2 | Otimo:  170 | Gulosa:  170 | Gap:   0.0%
Instancia  3 | Otimo:  155 | Gulosa:  155 | Gap:   0.0%
Instancia  4 | Otimo:  147 | Gulosa:  147 | Gap:   0.0%
Instancia  5 | Otimo:  261 | Gulosa:  261 | Gap:   0.0%
Instancia  6 | Otimo:  214 | Gulosa:  214 | Gap:   0.0%
Instancia  7 | Otimo:  191 | Gulosa:  187 | Gap:   2.1%
Instancia  8 | Otimo:  183 | Gulosa:  183 | Gap:   0.0%
Instancia  9 | Otimo:  215 | Gulosa:  206 | Gap:   4.2%
Instancia 10 | Otimo:  174 | Gulosa:  174 | Gap:   0.0%
Instancia 11 | Otimo:  262 | Gulosa:  262 | Gap:   0.0%
Instancia 12 | Otimo:  206 | Gulosa:  206 | Gap:   0.0%
Instancia 13 | Otimo:  231 | Gulosa:  231 | Gap:   0.0%
Instancia 14 | Otimo:  309 | Gulosa:  309 | Gap:   0.0%
Instancia 15 | Otimo:  294 | Gulosa:  294 | Gap:   0.0%
Instancia 16 | Otimo:  247 | Gulosa:  247 | Gap:   0.0%
Instancia 17 | Otimo:  136 | Gulosa:  134 | Gap:   1.5%
Instancia 18 | Otimo:  212 | Gulosa:  212 | Gap:   0.0%
Instancia 19 | Otimo:  243 | Gulosa:  243 | Gap:   0.0%
Instancia 20 | Otimo:  193 | Gulosa:  193 | Gap:   0.0%

===== RESUMO =====
Gap medio     : 0.39%
Gap minimo    : 0.00%
Gap maximo    : 4.19%
Desvio padrao : 1.03%
```

O **gap médio** obtido foi calculado comparando a solução gulosa com a solução ótima em 20 instâncias aleatórias. Gap igual a zero significa que a heurística encontrou o ótimo; quanto maior o percentual, maior a distância em relação ao melhor resultado possível. A heurística gulosa é rápida e costuma ser boa quando precisamos de uma resposta imediata, mas não garante o ótimo porque uma escolha local de alta densidade pode impedir uma combinação globalmente melhor. Para problemas pequenos ou decisões críticas, eu preferiria o método exato; para instâncias grandes ou aplicações com limite de tempo, usaria a heurística como solução inicial ou resposta aproximada.

## Atividade 4 — Modelagem de seleção de disciplinas

### Problema escolhido

O problema consiste em escolher quais disciplinas cursar no próximo semestre, maximizando uma medida de utilidade acadêmica e profissional, sem ultrapassar o limite de créditos e sem violar pré-requisitos.

### Modelagem formal

Uma solução candidata é um vetor binário com seis posições. O valor 1 indica que a disciplina será cursada e 0 indica que ela não será cursada. O espaço de busca possui `2^6 = 64` soluções possíveis. A função objetivo maximiza a soma das utilidades das disciplinas selecionadas. As restrições são: a soma dos créditos deve ser no máximo 12 e todos os pré-requisitos de uma disciplina selecionada precisam estar presentes na solução.

Este problema tem semelhança com o problema da mochila e tende a ser difícil em sua versão geral, porque o número de combinações cresce exponencialmente conforme aumentam as disciplinas e as restrições. Para seis disciplinas é possível enumerar todas as soluções, mas essa abordagem não escala bem.

### Resultado da execução do código

```text
PROBLEMA: selecao de disciplinas para o proximo semestre
Solucao aleatoria (0=nao cursa, 1=cursa): [0, 0, 1, 0, 0, 0]
Disciplinas: Banco de Dados
Creditos totais: 4
Utilidade total: 8
Solucao factivel: True
Espaco de busca: 64 solucoes
```

O código gera uma solução aleatória factível, calcula a utilidade e os créditos totais e verifica conjuntamente o limite de créditos e os pré-requisitos. Dessa forma, há correspondência direta entre a modelagem apresentada e a implementação.
