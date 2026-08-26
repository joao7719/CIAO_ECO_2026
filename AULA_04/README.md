# AULA 04 — AC-1 Parte Final



Esta pasta contém a implementação dos exercícios e desafios solicitados no roteiro da etapa final da AC-1.



## Arquivos



| Arquivo | Conteúdo |

| --- | --- |

| `exercicios_01_02.py` | Comparação do algoritmo genético com e sem elitismo e cálculo de penalidade de SLA. |

| `desafio_03_alocacao_servidores.py` | Balanceamento de 20 tarefas em quatro servidores com minimização do makespan. |

| `desafio_ac1_master_sdwan.py` | Motor de seleção de rota SD-WAN Zero-Trust para 12 roteadores. |



## Como executar



Os scripts utilizam Python 3 e NumPy. A execução pode ser feita com:



```bash

python3 AULA_04/exercicios_01_02.py

python3 AULA_04/desafio_03_alocacao_servidores.py

python3 AULA_04/desafio_ac1_master_sdwan.py

```



## Requisitos atendidos



O Exercício 1 implementa a chave `usar_elitismo` e permite comparar a preservação do melhor indivíduo com a execução sem elitismo. O Exercício 2 soma a latência dos enlaces e acrescenta `1000.0` ms para cada enlace acima do limite de `50.0` ms. O Desafio 03 representa cada indivíduo por 20 inteiros no intervalo `[0, 3]`, calcula as cargas acumuladas e minimiza o maior carregamento entre os quatro servidores.



O desafio de fechamento cria uma matriz de adjacência e atributos de latência, perda de pacotes e reputação para os 12 roteadores. A origem é o nó `0`, o destino é o nó `11`, a semente estocástica é `2026` e o fitness é calculado por `latência total + 20 × perda total + penalidade de segurança`. A penalidade de segurança é `5000` quando a rota contém qualquer nó com reputação inferior a `50`.



## Resultado de referência



Com a semente padrão, o Desafio 03 encontra makespan de `136.00 s`, com cargas `[135.0, 134.0, 136.0, 136.0]`. O motor SD-WAN seleciona uma rota sem nós não confiáveis e apresenta a justificativa da escolha no terminal.

