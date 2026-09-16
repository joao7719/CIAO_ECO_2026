# Resultados — Aula 06

## Laboratório 01

Execução determinística com semente 42. O algoritmo encontrou uma rota de menor custo entre o nó 0 e o nó 5, usando feromônio, custo heurístico, evaporação e depósito. Os gráficos `convergencia_lab01.png` e `feromonio_lab01.png` registram a evolução do custo e a memória coletiva.

**Respostas:**

1. O ACO usa várias formigas para explorar caminhos diferentes simultaneamente, evitando depender de uma única trajetória e aumentando a diversidade da busca.
2. Uma rota de menor custo recebe mais feromônio porque tem maior qualidade; isso aumenta a probabilidade de ser escolhida pelas formigas seguintes.
3. A evaporação impede que as primeiras escolhas dominem para sempre e permite que novas rotas influenciem a busca.

## Laboratório 02

Foram executadas as configurações base, `ALPHA` baixo/alto, `BETA` baixo/alto, evaporação lenta/rápida e cinco/cinquenta formigas. Os outputs completos estão no terminal de execução do arquivo `lab02_aula06_ciao.py`.

**Interpretação:** aumentar `ALPHA` aumenta a influência da experiência acumulada; aumentar `BETA` favorece custos menores; evaporação alta faz o algoritmo esquecer mais rapidamente; mais formigas ampliam a exploração, mas aumentam o custo computacional.

## Laboratório 03

As funções de atratividade, evaporação, depósito e construção de rota foram completadas. A atratividade usa `feromônio^ALPHA * (1/custo)^BETA`; assim, mais feromônio aumenta a atratividade. A visita a nós já presentes é impedida para evitar ciclos e garantir que a formiga avance em uma rota simples.

## Laboratório 04

Foi implementado o ACO do zero com matriz de custos, feromônio, múltiplas formigas, atualização, evaporação e gráfico de evolução (`evolucao_lab04.png`). O caminho encontrado foi `[0, 1, 2, 3, 4, 5]`, com custo 8; o algoritmo probabilístico pode encontrar esse caminho ou outro de custo equivalente.

**Questões finais:**

1. O feromônio funciona como memória coletiva: caminhos usados por boas soluções recebem reforço e tornam-se mais prováveis nas iterações seguintes.
2. Explorar significa testar caminhos ainda pouco conhecidos; aproveitar significa seguir caminhos já reforçados. O equilíbrio entre ambos evita convergência prematura.
3. Em uma rede maior, eu investigaria primeiro a construção da rota e a quantidade de formigas/iterações, pois são os pontos que mais impactam o custo computacional. Também avaliaria restringir candidatos a vizinhos válidos e usar estruturas esparsas.
