# Resultados — Aula 08

> Os roteiros não fornecem todos os dados necessários aos laboratórios 02 e 03, nem definem uma equação térmica completa para o laboratório 01. Para permitir execução e comparação reproduzíveis, as hipóteses adotadas estão declaradas abaixo e também documentadas nos scripts.

## Laboratório 01 — PSO para balanceamento dinâmico de carga

**Modelo adotado.** Pesos contínuos não negativos `W = [w1,…,w6]`, normalizados a cada iteração para que `sum(wi)=1`. A temperatura da zona `i` é modelada por `T_i = 25 + C_i × (6 wi)² °C`: 25 °C de base, os coeficientes térmicos fornecidos e um termo quadrático que representa o crescimento não linear do aquecimento com a concentração de tráfego. O fator 6 compara a carga de cada zona com uma divisão uniforme. O objetivo é `sum(wi × T_i)` acrescido de penalidade externa quadrática quando qualquer `T_i > 75 °C`.

O PSO foi implementado do zero, incluindo velocidade, posição, melhores posições individual (`pbest`) e global (`gbest`). Foram usados 300 ciclos, semente determinística e populações de 10, 30 e 50 partículas.

| Partículas | Fitness final | Distribuição W (AZ1…AZ6) | Soma | Maior temperatura |
|---:|---:|---|---:|---:|
| 10 | 69,181820 | [0,17094; 0,18726; 0,14546; 0,20226; 0,15667; 0,13741] | 1,000000000000 | 69,182 °C |
| 30 | 69,181820 | [0,17094; 0,18726; 0,14546; 0,20226; 0,15667; 0,13741] | 1,000000000000 | 69,182 °C |
| 50 | 69,181820 | [0,17094; 0,18726; 0,14546; 0,20226; 0,15667; 0,13741] | 1,000000000000 | 69,182 °C |

As três populações convergiram ao mesmo vetor neste problema e nesta semente. A maior temperatura ficou abaixo do limite crítico, e os testes do código verificam normalização e limite térmico. O histórico de convergência está em [`convergencia_lab01_aula08.png`](convergencia_lab01_aula08.png).

## Laboratório 02 — AG binário para seleção de microsserviços Edge

O enunciado exige 15 serviços, mas não traz sua tabela de valores, RAM e CPU. Foi criada uma instância didática explícita no código, usando os recursos disponíveis no nó como restrições simultâneas: 16 GB de RAM e 8 cores. Cada execução usou 120 indivíduos, 180 gerações, seleção por torneio, crossover de ponto único, mutação binária, elitismo e 12 sementes por estratégia.

| Serviço | Valor | RAM (GB) | CPU (cores) |
|---|---:|---:|---:|
| Auth | 18 | 2,5 | 1,2 |
| API | 16 | 2,0 | 1,0 |
| Cache | 14 | 3,0 | 0,8 |
| Busca | 13 | 1,5 | 0,8 |
| Pagamentos | 20 | 2,5 | 1,5 |
| Catálogo | 12 | 2,0 | 0,7 |
| Fila | 11 | 1,0 | 0,6 |
| Métricas | 8 | 1,0 | 0,5 |
| Recomendação | 15 | 2,5 | 1,3 |
| Imagens | 10 | 2,0 | 0,8 |
| Notificações | 9 | 1,0 | 0,5 |
| Perfil | 12 | 1,5 | 0,7 |
| Relatórios | 7 | 1,5 | 0,6 |
| Auditoria | 10 | 1,0 | 0,6 |
| Recomendador ML | 19 | 4,0 | 2,0 |

A estratégia **rígida** atribui fitness zero a indivíduos inviáveis. A estratégia **proporcional** aplica desconto linear conforme o excesso percentual de RAM e CPU. Valores agregados das 12 execuções:

| Estratégia | Melhor valor viável encontrado | Entropia genética média final | Fitness médio na última geração | Desvio-padrão médio na última geração |
|---|---:|---:|---:|---:|
| Penalidade rígida | 124 | 0,676 | 79,409 | 46,801 |
| Penalidade proporcional | 124 | 0,602 | 108,956 | 13,915 |

A penalidade rígida preservou maior diversidade nesta configuração (entropia média 0,676 contra 0,602). Ambas encontraram valor 124. A enumeração exata dos `2¹⁵` subconjuntos confirmou 124 como ótimo viável para a tabela assumida; uma combinação de ótimo é Auth, API, Busca, Catálogo, Fila, Métricas, Recomendação, Notificações, Perfil e Auditoria. O fitness proporcional é maior na última geração porque aceita candidatos ainda inviáveis com desconto; por isso, a comparação de resultado final também reporta explicitamente o melhor valor **viável**. Gráficos de fitness e diversidade: [`comparacao_lab02_aula08.png`](comparacao_lab02_aula08.png).

## Laboratório 03 — ACO para topologia de baixa latência

O roteiro não contém uma matriz `D` nem define os pares críticos. Como hipótese transparente e substituível, o script cria 10 coordenadas fixas e deriva uma matriz de latências simétrica em milissegundos a partir da distância euclidiana (`2 + 3,2 × distância`). O custo usado é a soma das latências dos nove enlaces da árvore geradora. Cada formiga adiciona apenas uma aresta entre componentes distintos, usando Union-Find; assim, ciclos são evitados e a solução tem conectividade garantida. A evaporação `rho=0,2` é aplicada por iteração e apenas as 20% melhores topologias depositam feromônio.

A melhor topologia encontrada contém as arestas `(0,1), (0,2), (2,3), (3,4), (3,5), (4,6), (5,7), (7,9), (8,9)`. Seu custo acumulado foi **78,29 ms**, frente a **138,72 ms** de média em 3.000 árvores geradas aleatoriamente: redução de **43,56%**. A melhor árvore aleatória da amostra custou 90,85 ms.

Matriz de adjacência (linhas/colunas correspondem aos switches 0–9):

```text
[[0 1 1 0 0 0 0 0 0 0]
 [1 0 0 0 0 0 0 0 0 0]
 [1 0 0 1 0 0 0 0 0 0]
 [0 0 1 0 1 1 0 0 0 0]
 [0 0 0 1 0 0 1 0 0 0]
 [0 0 0 1 0 0 0 1 0 0]
 [0 0 0 0 1 0 0 0 0 0]
 [0 0 0 0 0 1 0 0 0 1]
 [0 0 0 0 0 0 0 0 0 1]
 [0 0 0 0 0 0 0 1 1 0]]
```

A verificação automática confirmou 9 arestas, conectividade e ausência de ciclos. Evidência visual: [`topologia_lab03_aula08.png`](topologia_lab03_aula08.png).

## Arquivos entregues

- `lab01_aula08.py` — PSO, penalidade térmica e comparação de populações.
- `lab02_aula08.py` — AG, estratégias de penalidade e busca exata de referência.
- `lab03_aula08.py` — ACO, geração da matriz de latências e validação da árvore.
- `convergencia_lab01_aula08.png`, `comparacao_lab02_aula08.png` e `topologia_lab03_aula08.png` — gráficos e evidências.
