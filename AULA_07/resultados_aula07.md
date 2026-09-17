# Resultados — Aula 07

## Laboratório 01 — ACO com busca local 2-opt

**Execução:**

```text
[LAB 01 - SUCESSO] Melhor Caminho: [0, 1, 3, 4, 2, 0] | Custo: 70.0
[LAB 01] Custo inicial: 70.0 | Custo final: 70.0
```

**1. Como o uso da busca local 2-opt afeta o equilíbrio entre exploração e aproveitamento?**

O ACO realiza a exploração global ao construir rotas diferentes com base no feromônio e na heurística. Depois, a busca 2-opt faz o aproveitamento local: testa inversões de trechos e mantém aquelas que reduzem o custo. Assim, o algoritmo explora várias regiões do espaço e refina as soluções promissoras. O excesso de busca local pode reduzir a diversidade e causar convergência prematura, mas, neste caso, o 2-opt melhora a qualidade das rotas sem substituir a exploração das formigas.

**2. O que aconteceria com a convergência se `rho = 0.0`?**

Sem evaporação, todo feromônio depositado permaneceria indefinidamente. Rotas encontradas nas primeiras iterações poderiam dominar a probabilidade de escolha, mesmo que não fossem as melhores, reduzindo a exploração. A convergência tenderia a ocorrer mais cedo, porém com maior risco de convergência prematura e de ficar presa em uma solução subótima.

## Laboratório 02 — Algoritmo genético

**Execução:**

```text
[LAB 02 - SUCESSO] Melhor indivíduo: [0, 1, 1, 1, 1]
[LAB 02] Peso: 8 | Valor: 15
```

**1. Qual é o papel da mutação e o que ocorre com taxa de 100%?**

A mutação introduz diversidade genética, evita que a população fique uniforme e pode recuperar combinações que foram perdidas. Com taxa de 100%, cada gene seria invertido em toda reprodução. Isso gera forte aleatoriedade e pode destruir boas características, fazendo o algoritmo se comportar mais como uma busca aleatória; a pressão de seleção ainda existe, mas a convergência tende a ficar instável.

**2. Por que penalizar indivíduos acima da capacidade?**

Atribuir fitness zero aos indivíduos inviáveis impede que uma solução que exceda a capacidade seja escolhida por apresentar valor alto. Dessa forma, a seleção favorece soluções que respeitam a restrição e orienta a população para a região factível do espaço de busca. Sem a penalização, o algoritmo poderia convergir para respostas impossíveis.

## Laboratório 03 — PSO

**Execução:**

```text
[LAB 03 - SUCESSO] Melhor posição encontrada pelo Enxame (gbest): [ 0.00742668 -0.0130891 ]
[LAB 03] Fitness do gbest: 0.00022648
```

**1. O que ocorre se `c1 = 0`?**

A partícula deixa de ser atraída pelo próprio melhor ponto histórico. Ela passa a depender da inércia e da melhor posição coletiva (`gbest`). Isso reduz a memória individual e pode acelerar a convergência para a região conhecida pelo enxame, mas também reduz a diversidade e aumenta o risco de convergência prematura.

**2. Qual é a função da inércia `w`?**

A inércia controla quanto da velocidade anterior é preservado. Valores maiores favorecem deslocamentos mais longos e exploração global; valores menores reduzem o movimento e favorecem o refinamento local. Um valor equilibrado ajuda o enxame a explorar o espaço antes de se concentrar no mínimo.

## Laboratório 04 — ACO: feromônio, evaporação e atratividade

**Execução:**

```text
[LAB 04 - SUCESSO] Matriz de Feromônio Atualizada:
 [[0.75       0.91666667 0.91666667 0.75      ]
  [0.75       0.75       0.75       1.08333333]
  [0.75       0.91666667 0.75       0.75      ]
  [0.75       0.75       0.75       0.75      ]]
```

**1. Por que a evaporação é necessária no ACO?**

A evaporação reduz gradualmente a influência de decisões antigas. Ela evita que um caminho escolhido no início domine permanentemente e permite que novas rotas sejam exploradas. Portanto, contribui para o equilíbrio entre exploração e aproveitamento.

**2. O que ocorreria em grafos complexos sem evaporação? Qual é a relação entre latência e atratividade inicial?**

Sem evaporação, os feromônios se acumulam sem limite e o algoritmo pode ficar preso a uma rota inicial, dificultando a descoberta de alternativas melhores. A atratividade heurística é inversamente proporcional à latência: `eta_ij = 1 / latência_ij` (ou, quando há influência ajustável, `eta_ij = (1 / latência_ij)^beta`). Assim, enlaces de menor latência são mais atrativos.

## Laboratório 05 — Algoritmo memético

**Execução:**

```text
[LAB 05 - SUCESSO] Solução Inicial: [ 2.5 -3.1] | Fitness: 37.7698
[LAB 05] Solução Refinada: [ 2.47553974 -3.04650038] | Fitness: 35.7154
```

**1. Qual é a diferença entre um algoritmo genético puro e um algoritmo memético?**

O algoritmo genético puro usa principalmente mecanismos populacionais, como seleção, crossover e mutação. O algoritmo memético combina essa busca global com busca local aplicada às soluções, refinando-as individualmente antes da próxima etapa. Ele tende a obter soluções mais precisas, ao custo de mais processamento.

**2. Qual é o impacto computacional de aplicar busca local a todos os indivíduos em cada geração?**

O custo computacional aumenta porque cada indivíduo exige várias avaliações adicionais da função objetivo. Se a população tem tamanho `P`, são executadas `G` gerações e a busca local faz `S` passos, o custo adicional é aproximadamente `O(P × G × S)` avaliações, além do custo do algoritmo evolutivo. A intensificação pode acelerar a qualidade da solução, mas deve ser equilibrada com o orçamento computacional.

## Arquivos entregues

- `lab01_aula07.py` — ACO híbrido e gráfico de convergência.
- `lab02_aula07.py` — algoritmo genético com seleção, crossover e mutação.
- `lab03_aula07.py` — PSO com inércia, componente cognitiva e componente social.
- `lab04_aula07.py` — evaporação e depósito de feromônio.
- `lab05_aula07.py` — busca local hill climbing para Rastrigin.
