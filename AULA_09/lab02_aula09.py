"""Aula 09 / Lab 02 — gorjeta fuzzy e experimentos solicitados no roteiro.
Mamdani com min (AND), max (OR), agregação max e centroide discreto.
Execução: python3 lab02_aula09.py. Requer numpy e matplotlib.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fuzzy_utils import trimf,trapmf,aggregate
OUT=Path(__file__).resolve().parent

def controller(servico,comida,rule_variant="baseline",shape="triangular",method="centroid",excellent=False,plot=False):
    if not (0<=servico<=10 and 0<=comida<=10): raise ValueError("Notas devem estar entre 0 e 10.")
    x=np.arange(0,10.001,.05); y=np.arange(0,25.001,.1)
    def sets(universe,tri):
        if shape=="trapezoidal": return {"ruim":trapmf(universe,[0,0,2.5,5.5]),"medio":trapmf(universe,[3.5,4.5,5.5,6.5]),"bom":trapmf(universe,[4.5,7.5,10,10])}
        return {"ruim":trimf(universe,[0,0,5]),"medio":trimf(universe,[0,5,10]),"bom":trimf(universe,[5,10,10])}
    s,c=sets(x,True),sets(x,True)
    sm={k:float(np.interp(servico,x,m)) for k,m in s.items()}; cm={k:float(np.interp(comida,x,m)) for k,m in c.items()}
    tip={"baixa":trimf(y,[0,0,13]),"media":trimf(y,[0,13,25]),"alta":trimf(y,[13,25,25])}
    if excellent:
        s["excelente"]=trapmf(x,[7.5,9,10,10]); sm["excelente"]=float(np.interp(servico,x,s["excelente"]))
    # Regras do roteiro: OR para extremos; alternativa experimental troca médio por AND.
    rules=[(max(sm["ruim"],cm["ruim"]),tip["baixa"])]
    if rule_variant=="baseline": rules.append((sm["medio"],tip["media"]))
    elif rule_variant=="and_medio": rules.append((min(sm["medio"],cm["medio"]),tip["media"]))
    else: raise ValueError("rule_variant deve ser baseline ou and_medio")
    rules.append((max(sm["bom"],cm["bom"]),tip["alta"]))
    if excellent: rules.append((sm["excelente"],tip["alta"]))
    agg,out=aggregate(y,rules,method)
    if plot:
        fig,ax=plt.subplots(1,3,figsize=(13,3.8))
        for k,m in s.items():ax[0].plot(x,m,label=k)
        for k,m in c.items():ax[1].plot(x,m,label=k)
        for k,m in tip.items():ax[2].plot(y,m,label=k)
        ax[2].fill_between(y,0,agg,color="#5aa9e6",alpha=.45);ax[2].axvline(out,color="red",ls="--",label=f"{method}={out:.2f}%")
        for a,t in zip(ax,["Serviço","Comida","Gorjeta"]):a.set(title=t,xlabel="Nota" if t!="Gorjeta" else "Percentual (%)",ylabel="μ");a.grid(alpha=.2);a.legend(fontsize=8)
        fig.tight_layout();fig.savefig(OUT/"fuzzy_lab02_aula09.png",dpi=160);plt.close(fig)
    return out

def main():
    casos=[(9.8,6.5),(7,3),(0,0),(10,10),(5,5)]
    for s,c in casos:print(f"serviço={s:>4g}, comida={c:>4g} -> gorjeta={controller(s,c):.2f}%")
    base=controller(7,3); alterada=controller(7,3,rule_variant="and_medio")
    trap=controller(9.8,6.5,shape="trapezoidal"); mom=controller(9.8,6.5,method="mom"); gaussproxy=controller(9.8,6.5,shape="trapezoidal",excellent=True)
    print(f"Experimento médio OR/antecedente vs AND: (7,3) {base:.2f}% -> {alterada:.2f}%")
    print(f"Triangular vs trapezoidal (9.8,6.5): {controller(9.8,6.5):.2f}% vs {trap:.2f}%")
    print(f"Centroide vs média dos máximos: {controller(9.8,6.5):.2f}% vs {mom:.2f}%")
    print(f"Com conjunto excelente (9.8,6.5): {gaussproxy:.2f}%")
    controller(9.8,6.5,plot=True);print("[OK] funções de pertinência e agregação salvas.")
if __name__=="__main__":main()
