# Resultados — Aula 09: Lógica Fuzzy

## Implementação e escolhas de modelagem

Os laboratórios foram implementados em Python com NumPy e Matplotlib e executam sem dependência externa de `scikit-fuzzy`. O módulo `fuzzy_utils.py` contém funções triangulares/trapezoidais, agregação Mamdani por máximo, implicação por mínimo e defuzzificação por centroide (além de média/mínimo dos máximos para o experimento do lab 02). O centroide usa integração numérica no universo discretizado.

Os universos foram escolhidos de acordo com as unidades naturais de cada problema: temperatura do ventilador de 0–40 °C e saída 0–100%; gorjeta 0–25% e notas de serviço/comida 0–10; evasão com frequência, desempenho e risco de 0–100%. Ombros trapezoidais nos extremos mantêm pertinência plena perto dos limites físicos; triângulos representam categorias intermediárias com pico nítido e sobreposição gradual. A sobreposição evita transições abruptas entre termos linguísticos. Os parâmetros são hipóteses didáticas transparentes no código e podem ser ajustados com dados reais.

## Laboratório 01 — Ventilador fuzzy

Entradas: temperatura, com termos `frio`, `morno` e `quente`. Saída: velocidade, com termos `baixa`, `media` e `alta`. Regras: SE temperatura é fria ENTÃO velocidade baixa; SE morna ENTÃO média; SE quente ENTÃO alta. As categorias externas usam trapézios e a categoria central usa triângulo; o centroide converte a saída fuzzy em percentual nítido.

| Temperatura | Velocidade sugerida |
|---:|---:|
| 10 °C | 16,67% |
| 20 °C | 44,05% |
| 25 °C | 50,00% |
| 30 °C | 55,95% |
| 38 °C | 83,33% |

A saída cresce gradualmente conforme a temperatura; o valor não muda por um único limiar booleano. Gráfico das pertinências e do consequente agregado: [`fuzzy_lab01_aula09.png`](fuzzy_lab01_aula09.png).

## Laboratório 02 — Gorjeta

Universos: serviço e comida de 0–10 pontos; gorjeta de 0–25%. Entradas usam conjuntos `ruim`, `medio` e `bom`; a saída usa `baixa`, `media` e `alta`. As regras-base seguem o roteiro: (1) serviço ruim OU comida ruim → gorjeta baixa; (2) serviço médio → média; (3) serviço bom OU comida boa → alta. AND usa mínimo, OR usa máximo e a saída é defuzzificada pelo centroide.

| Serviço | Comida | Saída calculada | Leitura qualitativa |
|---:|---:|---:|---|
| 9,8 | 6,5 | 19,86% | gorjeta alta; próximo ao exemplo didático de 20,2% |
| 7 | 3 | 12,55% | moderada, com regras baixa/média/alta parcialmente ativadas |
| 0 | 0 | 4,33% | baixa |
| 10 | 10 | 21,00% | alta |
| 5 | 5 | 12,67% | média |

A pequena diferença em relação aos 20,2% do exemplo decorre dos formatos/parâmetros discretizados escolhidos nesta implementação; o exemplo do material não especifica todas as coordenadas das funções de pertinência. O teste troca a regra média, variando-a de “serviço médio” para “serviço médio E comida média”; para (7,3), o resultado permanece 12,55% porque ambas as notas têm pertinência média 0,6, e as ativações dos termos baixo/alto são simétricas. O uso de conjuntos trapezoidais alterou a saída de (9,8;6,5) para 21,00%. O método média dos máximos gerou 24,80%, mais extremo que o centroide (19,86%) porque considera apenas os pontos de máxima pertinência. A inclusão de “excelente” como termo adicional foi testada.

Evidência das pertinências e da área agregada: [`fuzzy_lab02_aula09.png`](fuzzy_lab02_aula09.png).

## Laboratório 03 — Risco de evasão acadêmica

**Problema (definição).** A equipe pedagógica precisa priorizar conversas de acompanhamento, sem tratar uma única nota de corte como decisão automática. As entradas são frequência e desempenho acadêmico, em porcentagens de 0–100; a saída é risco estimado de evasão, também de 0–100%. A lógica fuzzy é adequada porque frequência e notas baixas elevam o alerta gradualmente e em conjunto, e porque há situações intermediárias que não cabem bem em categorias rígidas.

**Modelagem.** Para frequência, os termos são `baixa` (trapézio [0,0,55,75]), `media` (triângulo [55,75,90]) e `alta` (trapézio [80,92,100,100]). Para desempenho, `baixa` = [0,0,45,65], `media` = [45,65,82] e `alta` = [70,85,100,100]. A saída contém `baixo` = [0,0,20,45], `medio` = [25,50,75] e `alto` = [55,75,100,100]. As regras completas implementadas são:

1. SE frequência baixa **OU** desempenho baixo, ENTÃO risco alto.
2. SE frequência média **E** desempenho baixo, ENTÃO risco alto.
3. SE frequência baixa **E** desempenho médio, ENTÃO risco alto.
4. SE frequência alta **E** desempenho alto, ENTÃO risco baixo.
5. SE frequência alta **E** desempenho médio, ENTÃO risco médio.
6. SE frequência média **E** desempenho alto, ENTÃO risco médio.
7. SE frequência média **E** desempenho médio, ENTÃO risco médio.
8. SE frequência alta **E** desempenho baixo, ENTÃO risco médio.
9. SE frequência baixa **E** desempenho alto, ENTÃO risco médio.

Os testes cobrem situações típicas, limítrofes/intermediárias e combinações discordantes:

| Situação | Frequência | Desempenho | Risco fuzzy | Expectativa qualitativa |
|---|---:|---:|---:|---|
| Acompanhamento forte | 98% | 92% | 17,05% | baixo |
| Bom desempenho geral | 85% | 78% | 33,49% | baixo a médio |
| Situação intermediária | 70% | 60% | 58,28% | médio |
| Alerta crítico | 35% | 40% | 82,03% | alto |
| Baixa frequência, boa nota | 40% | 90% | 69,01% | médio a alto; frequência fraca aciona alerta |

O controlador deve apoiar, não substituir, avaliação humana. Os gráficos gerados são [`fuzzy_lab03_aula09_pertinencias.png`](fuzzy_lab03_aula09_pertinencias.png) e [`fuzzy_lab03_aula09_superficie.png`](fuzzy_lab03_aula09_superficie.png).

## Execução e arquivos entregues

Todos os laboratórios executaram sem erro e geraram suas figuras. Os scripts foram compilados com `py_compile`.

- `lab01_aula09.py` — conjuntos fuzzy e controlador de ventilador.
- `lab02_aula09.py` — gorjeta, regras alternativas, forma das pertinências e defuzzificação.
- `lab03_aula09.py` — sistema próprio para risco de evasão, 9 regras e testes.
- `fuzzy_utils.py` — funções compartilhadas de pertinência e inferência Mamdani.
- `lab03_aula09.txt` — enunciado original do projeto, preservado junto à implementação.
- `fuzzy_lab01_aula09.png`, `fuzzy_lab02_aula09.png` e duas figuras do lab 03 — evidências dos conjuntos, resultados e superfície.

**Observação:** o roteiro também pede enviar por e-mail o link da aula 09 ao professor. O material não fornece o endereço do destinatário e nenhum e-mail foi enviado; os artefatos foram preparados e publicados no repositório solicitado.
