# Resultados — AC-2 Aula 05: Particle Swarm Optimization

## Entregáveis e metodologia

Foi elaborado um notebook único com as quatro missões do roteiro. Todas as implementações foram executadas com sementes fixas para permitir a reprodução dos resultados. Na Missão 3, foi usada a convenção mais direta de **fitness igual ao custo positivo**, pois o objetivo é minimizá-lo; essa escolha evita a inconsistência do esqueleto que retornava custo negativo e depois selecionava o menor valor.

## Missão 1 — A partícula solitária

A função objetivo foi `f(x) = x²`, com domínio `[-10, 10]`, `w = 0,8`, `c1 = 1,5`, `c2 = 1,5` e 20 iterações.

| Medida | Resultado |
|---|---:|
| Posição inicial | 8,459271 |
| Fitness inicial | 71,559259 |
| Melhor posição encontrada | 7,462724 |
| Melhor fitness encontrado | 55,692246 |
| Iterações executadas | 20 |

**Conclusão:** não encontrou o mínimo global `x = 0` nas 20 iterações. Isso ocorre porque, com apenas uma partícula, `pBest` e `gBest` são iguais à própria memória inicial; não existe cooperação com outras posições. A dificuldade foi considerada **média**, pois a implementação da fórmula é simples, mas o comportamento evidencia a limitação de uma partícula isolada.

## Missão 2 — O enxame na função de Rosenbrock

A função usada foi `f(x,y) = (1-x)² + 100(y-x²)²`, com 20 partículas e 50 iterações. O ótimo global é `(1, 1)`.

| Medida | Resultado |
|---|---:|
| Melhor posição encontrada | (1,0055; 1,0104) |
| Fitness final | 0,0000618403 |
| Distância até o ótimo `(1,1)` | 0,011768 |

**Conclusão:** o enxame encontrou uma solução muito próxima do mínimo global. Em comparação com a Missão 1, o enxame foi mais eficaz porque mantém várias soluções candidatas e usa `gBest` para compartilhar informação. A dificuldade foi considerada **média**.

## Missão 3 — Problema corporativo de logística

Foram gerados 50 clientes em uma região `10 × 10`, com cinco centros de distribuição, 30 partículas e 100 iterações. O custo de cada cliente foi calculado como a distância até o centro mais próximo multiplicada pela demanda.

| Medida | Resultado |
|---|---:|
| Custo inicial | 4.159,95 |
| Custo final | 3.445,44 |
| Melhoria | 17,18% |
| Centros alocados | 5 |

Centros encontrados:

| Centro | X | Y |
|---|---:|---:|
| 1 | 1,627 | 5,100 |
| 2 | 6,460 | 4,100 |
| 3 | 7,521 | 7,695 |
| 4 | 7,783 | 1,938 |
| 5 | 3,915 | 1,239 |

**Conclusão:** o custo melhorou em relação à melhor solução inicial do enxame. Os cinco centros foram mantidos e distribuídos por regiões diferentes para reduzir as distâncias ponderadas pelas demandas. A dificuldade foi considerada **média**.

## Missão 4 — Otimização dos parâmetros

Cada configuração foi executada cinco vezes sobre os mesmos dados, com sementes diferentes. A tabela mostra os valores médios obtidos.

| Experimento | Custo médio | Desvio-padrão | Melhor custo | Pior custo |
|---|---:|---:|---:|---:|
| Padrão | 3.374,33 | 79,06 | 3.290,20 | 3.524,28 |
| Inércia Alta (`w=0,9`) | 3.773,33 | 191,67 | 3.447,09 | 4.036,77 |
| Inércia Baixa (`w=0,5`) | 3.234,97 | 3,74 | 3.232,02 | 3.242,28 |
| Cognitivo Alto (`c1=2,5`) | 3.552,64 | 122,46 | 3.427,57 | 3.707,55 |
| Social Alto (`c2=2,5`) | 3.695,95 | 35,87 | 3.628,58 | 3.733,42 |
| Mais Partículas (`60`) | 3.370,72 | 116,32 | 3.254,61 | 3.572,43 |

**Melhor configuração encontrada:** `w = 0,5`, `c1 = 1,8`, `c2 = 1,8`, `30` partículas, com custo médio de **3.234,97**.

**Pior configuração encontrada:** `w = 0,9`, `c1 = 1,8`, `c2 = 1,8`, `30` partículas, com custo médio de **3.773,33**.

A inércia alta manteve mais movimento e exploração, mas dificultou a estabilização. A inércia baixa favoreceu o refinamento local e apresentou, neste experimento, o menor custo médio e a menor variabilidade. Aumentar `c1` tornou a busca mais dependente da experiência individual e piorou o resultado médio. Aumentar `c2` intensificou a atração pelo melhor global, mas reduziu a diversidade e também apresentou resultado inferior ao padrão. Aumentar o número de partículas ampliou a amostragem do espaço, porém não compensou o comportamento dos demais parâmetros neste conjunto de sementes.

A recomendação para este problema é a configuração de **inércia baixa (`w=0,5`)**, mantendo `c1=c2=1,8` e 30 partículas, porque apresentou o menor custo médio e alta estabilidade entre as cinco execuções.

## Relatório final

### O que é PSO e como funciona?

PSO é uma meta-heurística de inteligência coletiva inspirada no comportamento de grupos, como bandos de pássaros. Cada partícula representa uma solução candidata e possui uma posição, uma velocidade e uma memória da melhor posição que já visitou. A cada iteração, a velocidade combina a inércia, a atração pela melhor posição pessoal e a atração pela melhor posição do enxame. Em seguida, a partícula se move, é avaliada e atualiza suas memórias.

### Diferença entre `pBest` e `gBest`

`pBest` é a melhor solução encontrada por uma partícula individualmente. `gBest` é a melhor solução encontrada por qualquer partícula do enxame. `pBest` preserva a experiência local e ajuda a explorar trajetórias diferentes; `gBest` compartilha a melhor descoberta e orienta a convergência coletiva.

### Respostas resumidas do roteiro

| Missão | Resposta | Dificuldade |
|---|---|---|
| 1 — Partícula solitária encontrou o mínimo? | Não, em 20 iterações; melhor `x = 7,462724` | Média |
| 2 — Enxame encontrou o mínimo global? | Sim, com fitness `0,0000618403`, próximo de `(1,1)` | Média |
| 2 — Foi mais rápido/eficaz que a Missão 1? | Sim, por explorar várias partículas e usar `gBest` | — |
| 3 — O custo melhorou? | Sim, de `4.159,95` para `3.445,44` | Média |
| 3 — Quantos centros foram alocados? | 5 | — |
| 4 — Melhor configuração | `w=0,5`, `c1=1,8`, `c2=1,8`, 30 partículas | Média |
| 4 — Pior configuração | `w=0,9`, `c1=1,8`, `c2=1,8`, 30 partículas | — |

A principal dificuldade foi manter a lógica de minimização consistente e interpretar corretamente o papel de `pBest` e `gBest`. A atividade mostrou que regras simples de movimento, combinadas com memória e cooperação, podem resolver funções matemáticas e um problema logístico de localização.

## Arquivo executado

O notebook contém o código completo, as visualizações e os outputs gerados durante a execução: `atividades_aula05.ipynb`.
