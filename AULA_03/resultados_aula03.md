# Resultados e considerações — Aula 3

Este relatório reúne as execuções dos três laboratórios da Aula 3. As notebooks usam sementes aleatórias para tornar os resultados reproduzíveis; pequenas diferenças podem ocorrer quando os códigos são executados novamente sem a semente.

## Laboratório 1 — Algoritmo genético para x²

### Saída da execução

```text
==================================================
ALGORITMO GENÉTICO PASSO A PASSO
==================================================

População inicial: [[0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0], [0, 1, 0, 1, 1], [0, 0, 1, 1, 1], [0, 0, 1, 0, 0]]

==================== GERAÇÃO 0 ====================

Avaliação dos indivíduos:
  [0, 0, 1, 0, 0] → x= 4 → f(x)= 16
  [0, 0, 0, 1, 0] → x= 2 → f(x)=  4
  [0, 0, 0, 0, 0] → x= 0 → f(x)=  0
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 0, 1, 1, 1] → x= 7 → f(x)= 49
  [0, 0, 1, 0, 0] → x= 4 → f(x)= 16

 Melhor: x = 11 → f(x) = 121

==================== GERAÇÃO 1 ====================

Avaliação dos indivíduos:
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 0, 1, 1, 1] → x= 7 → f(x)= 49
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 0, 1, 1, 1] → x= 7 → f(x)= 49

 Melhor: x = 11 → f(x) = 121

==================== GERAÇÃO 2 ====================

Avaliação dos indivíduos:
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 0, 1, 1, 1] → x= 7 → f(x)= 49

 Melhor: x = 15 → f(x) = 225

==================== GERAÇÃO 3 ====================

Avaliação dos indivíduos:
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 1, 0, 1, 0] → x=10 → f(x)=100

 Melhor: x = 15 → f(x) = 225

==================== GERAÇÃO 4 ====================

Avaliação dos indivíduos:
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 1, 0, 1, 1] → x=11 → f(x)=121
  [0, 1, 1, 0, 1] → x=13 → f(x)=169
  [0, 1, 0, 0, 1] → x= 9 → f(x)= 81
  [0, 1, 1, 1, 1] → x=15 → f(x)=225

 Melhor: x = 15 → f(x) = 225

==================== GERAÇÃO 5 ====================

Avaliação dos indivíduos:
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [0, 1, 1, 1, 1] → x=15 → f(x)=225
  [0, 1, 1, 1, 1] → x=15 → f(x)=225

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 6 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [0, 0, 1, 1, 1] → x= 7 → f(x)= 49
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [1, 1, 1, 0, 0] → x=28 → f(x)=784
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 1, 0] → x=30 → f(x)=900

 Melhor: x = 31 → f(x) = 961

==================== GERAÇÃO 7 ====================

Avaliação dos indivíduos:
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 1, 1, 0] → x=30 → f(x)=900
  [1, 1, 0, 0, 1] → x=25 → f(x)=625
  [1, 1, 1, 1, 1] → x=31 → f(x)=961
  [1, 1, 0, 1, 1] → x=27 → f(x)=729
  [0, 1, 1, 0, 0] → x=12 → f(x)=144

 Melhor: x = 31 → f(x) = 961

==================================================
RESULTADO FINAL
==================================================

Melhor indivíduo: [1, 1, 1, 1, 1]
x = 31
f(x) = 961

Ótimo global: x = 31, f(x) = 961
Erro: 0
```

O cromossomo possui 5 bits, portanto representa valores inteiros de 0 a 31. O objetivo é maximizar `x²`, cujo ótimo global ocorre em `x = 31`, com valor 961. O elitismo preserva o melhor indivíduo de cada geração, enquanto seleção por roleta, crossover e mutação exploram o espaço de busca. A representação binária é adequada porque permite testar diretamente como operadores genéticos transformam soluções.

## Laboratório 2 — OneMax

### Saída da execução padrão

```text
==================================================
ONEMAX - AG com 30 indivíduos, 50 gerações
==================================================
Geração   0: Melhor = 14/20, Média = 9.80
Geração  10: Melhor = 20/20, Média = 18.90
Geração  20: Melhor = 20/20, Média = 19.50
Geração  30: Melhor = 20/20, Média = 19.43
Geração  40: Melhor = 20/20, Média = 19.53

 MELHOR FITNESS: 20/20
   Ótimo = 20 (todos os bits são 1)

==================================================
DESAFIO: Mude os parâmetros e veja o que acontece!
==================================================
1. Aumente a TAXA_MUT para 0.1. O que acontece?
2. Diminua POPULACAO para 10. O que acontece?
3. Aumente GERACOES para 100. O que acontece?
4. Mude ELITE para 0. O que acontece?
```

No problema OneMax, o fitness é simplesmente a quantidade de bits 1. O ótimo global é 20/20. A população tende a melhorar ao longo das gerações, e o elitismo impede que a melhor solução já encontrada seja perdida.

### Experimentos do desafio

| Configuração | População | Gerações | Mutação | Elitismo | Melhor fitness |
|---|---:|---:|---:|---:|---:|
| Configuração padrão | 30 | 50 | 0.02 | 2 | 20/20 |
| Mutação alta | 30 | 50 | 0.10 | 2 | 20/20 |
| População pequena | 10 | 50 | 0.02 | 2 | 20/20 |
| Mais gerações | 30 | 100 | 0.02 | 2 | 20/20 |
| Sem elitismo | 30 | 50 | 0.02 | 0 | 20/20 |

Aumentar a taxa de mutação aumenta a exploração, mas pode dificultar a convergência quando fica excessiva. Reduzir a população diminui a diversidade e pode causar convergência prematura. Aumentar o número de gerações oferece mais tempo para evolução. Retirar o elitismo permite maior diversidade, porém também pode perder a melhor solução encontrada.

## Laboratório 3 — Otimização de x·sen(3x)

### Saída da execução

```text
==================================================
OTIMIZANDO f(x) = x * sin(3x)
==================================================
Geração   0: Melhor f(x) = 6.2209 (x = 9.1765)
Geração  10: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  20: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  30: Melhor f(x) = 8.9019 (x = 8.9020)
Geração  40: Melhor f(x) = 8.9019 (x = 8.9020)

 MELHOR SOLUÇÃO: x = 8.9020, f(x) = 8.9019
```

As funções completadas foram `bits_para_x`, `fitness` e `mutacao`. A conversão transforma o valor inteiro de 8 bits, entre 0 e 255, em um ponto real no intervalo [0, 10]. O fitness usa a função objetivo e limita valores negativos a zero, pois a seleção por roleta precisa de pesos não negativos; isso não altera a solução ótima, que possui valor positivo. A mutação foi implementada como bit-flip e retorna uma cópia do indivíduo.

O AG procura uma boa aproximação do máximo global da função, que pode ser comparada com uma varredura numérica do intervalo. A solução encontrada pelo algoritmo deve ser interpretada como aproximada, pois a natureza aleatória dos operadores genéticos não garante o ótimo em todas as execuções.

## Conclusão

A Aula 3 mostrou como um algoritmo genético representa soluções, avalia indivíduos, seleciona pais, combina cromossomos, aplica mutações e preserva elites. Os experimentos também evidenciam que os parâmetros alteram o equilíbrio entre exploração e aproveitamento das melhores soluções.
