# Relatório Final PSO — Aula 05

## Entregáveis

Este relatório acompanha o notebook `atividades_aula05.ipynb`, organizado em uma seção curta para cada missão. O notebook foi executado integralmente sem erros, usando sementes fixas para tornar os resultados reproduzíveis.

## Missão 1 — Partícula solitária

A função objetivo foi `f(x) = x²`, no intervalo `[-10, 10]`, com 20 iterações. A partícula começou em aproximadamente `x = 8,4593` e terminou com melhor posição `x = 7,4627`, obtendo fitness `55,6922`.

A partícula **não encontrou o mínimo global** `x = 0` nas 20 iterações. Com apenas uma partícula não há diversidade nem cooperação; `pBest` e `gBest` representam essencialmente a mesma experiência. A dificuldade foi considerada **média**.

## Missão 2 — Enxame e Rosenbrock

O enxame utilizou 20 partículas durante 50 iterações para minimizar `(1-x)² + 100(y-x²)²`. O resultado foi uma posição próxima de `(1,1)`, com fitness muito próximo de zero.

O enxame foi mais eficaz que a partícula solitária porque várias soluções exploram o espaço simultaneamente e compartilham a melhor posição global. A dificuldade foi considerada **média**.

## Missão 3 — Problema logístico

Foram utilizados 50 clientes, demandas aleatórias, cinco centros, 30 partículas e 100 iterações. O custo considera a distância do cliente ao centro mais próximo multiplicada pela demanda.

| Medida | Resultado |
|---|---:|
| Custo inicial | 4.159,95 |
| Custo final | 3.314,91 |
| Melhoria | 20,31% |
| Centros alocados | 5 |

Centros encontrados:

| Centro | X | Y |
|---|---:|---:|
| 1 | 5,704 | 7,765 |
| 2 | 7,521 | 2,752 |
| 3 | 8,366 | 7,131 |
| 4 | 1,595 | 5,151 |
| 5 | 4,437 | 2,275 |

O custo **melhorou** em relação à solução inicial. A dificuldade foi considerada **média**.

## Missão 4 — Parâmetros

Cada configuração foi testada cinco vezes. A tabela com os valores de custo médio, desvio-padrão, melhor e pior resultado é exibida no notebook.

| Item | Resultado |
|---|---|
| Melhor configuração | Mais partículas — 60 partículas, `w=0,7`, `c1=1,8`, `c2=1,8` |
| Pior configuração | Inércia alta — 30 partículas, `w=0,9`, `c1=1,8`, `c2=1,8` |

A inércia alta manteve as partículas se movimentando por mais tempo, mas dificultou a convergência. A inércia baixa favorece a busca local. Um `c1` maior aumenta a influência da memória individual; um `c2` maior aumenta a influência do melhor global. Mais partículas aumentam a diversidade e, neste experimento, produziram o melhor custo médio, embora aumentem o tempo de execução. A configuração recomendada é **Mais partículas**, pois apresentou o menor custo médio entre as opções testadas.

## Relatório final — conceitos

**O que é PSO?** PSO é uma técnica de inteligência coletiva na qual cada partícula representa uma solução candidata. A partícula atualiza sua velocidade considerando a direção anterior, sua melhor posição pessoal e a melhor posição encontrada pelo grupo. Depois, atualiza sua posição e calcula novamente o fitness.

**Diferença entre `pBest` e `gBest`.** `pBest` é a melhor posição que uma partícula encontrou individualmente. `gBest` é a melhor posição encontrada por qualquer partícula do enxame. `pBest` mantém a experiência individual, enquanto `gBest` promove a cooperação e direciona o enxame.

**Conclusão.** A atividade mostrou a evolução do PSO desde uma partícula isolada até uma aplicação logística. O enxame é mais eficiente porque combina exploração de várias soluções com memória individual e informação social. Na logística, o algoritmo reduziu o custo em 20,31% e posicionou cinco centros para atender os clientes.

**Dificuldade geral:** média. A parte mais importante foi manter a atualização de velocidade vetorial e a função de custo coerentes com o objetivo de minimização.
