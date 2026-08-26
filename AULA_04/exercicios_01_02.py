"""Exercícios 1 e 2 da etapa final da AC-1."""



from __future__ import annotations



import numpy as np





def calcular_custo(rota: np.ndarray, matriz: np.ndarray) -> float:
  
    """Custo de uma rota fechada, incluindo o retorno ao primeiro nó."""
  
    return float(sum(matriz[rota[i], rota[(i + 1) % len(rota)]] for i in range(len(rota))))
  




def executar_elitismo(usar_elitismo: bool, semente: int = 2026) -> float:
  
    """Executa o Exercício 1 com ou sem preservação do melhor indivíduo."""
  
    rng = np.random.default_rng(semente)
  
    num_nos, tamanho_pop, geracoes = 8, 40, 80
  
    matriz = rng.uniform(10, 100, (num_nos, num_nos))
  
    populacao = [rng.permutation(num_nos) for _ in range(tamanho_pop)]
  
    for _ in range(geracoes):
      
        custos = np.array([calcular_custo(ind, matriz) for ind in populacao])
      
        novos: list[np.ndarray] = []
      
        if usar_elitismo:
          
            novos.append(populacao[int(np.argmin(custos))].copy())
          
        while len(novos) < tamanho_pop:
          
            i1, i2 = rng.choice(tamanho_pop, 2, replace=False)
          
            pai = populacao[int(i1 if custos[i1] < custos[i2] else i2)].copy()
          
            if rng.random() < 0.3:
              
                j1, j2 = rng.choice(num_nos, 2, replace=False)
              
                pai[j1], pai[j2] = pai[j2], pai[j1]
              
            novos.append(pai)
          
        populacao = novos
      
    return min(calcular_custo(ind, matriz) for ind in populacao)
  




def calcular_custo_com_sla(rota: np.ndarray, matriz: np.ndarray,
                           
                           limite_sla: float = 50.0,
                           
                           penalidade_por_violacao: float = 1000.0) -> float:
                             
    """Soma latências consecutivas e multa cada enlace acima do SLA."""
                             
    custo_total = 0.0
                             
    penalidade = 0.0
                             
    for origem, destino in zip(rota[:-1], rota[1:]):
      
        latencia = float(matriz[origem, destino])
      
        custo_total += latencia
      
        if latencia > limite_sla:
          
            penalidade += penalidade_por_violacao
          
    return custo_total + penalidade
                             




def executar_sla() -> float:
  
    rng = np.random.default_rng(15)
  
    matriz_latencia = rng.uniform(5, 80, (6, 6))
  
    return calcular_custo_com_sla(np.array([0, 1, 2, 3, 4, 5]), matriz_latencia)
  




def main() -> None:
  
    com = executar_elitismo(True)
  
    sem = executar_elitismo(False)
  
    sla = executar_sla()
  
    print(f"[Exercício 1] Menor custo com elitismo: {com:.2f}")
  
    print(f"[Exercício 1] Menor custo sem elitismo: {sem:.2f}")
  
    print(f"[Exercício 2] Custo total com penalizações de SLA: {sla:.2f} ms")
  




if __name__ == "__main__":
  
    main()
  




__all__ = ["calcular_custo", "executar_elitismo", "calcular_custo_com_sla", "executar_sla"]

















































