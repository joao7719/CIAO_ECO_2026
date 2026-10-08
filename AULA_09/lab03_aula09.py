"""Aula 09 / Lab 03 — inferência fuzzy do risco de evasão acadêmica.
Entradas: frequência e desempenho (0–100%); saída: risco (0–100%).
Universos, pertinências e regras são modelados explicitamente neste arquivo.
Execução: python3 lab03_aula09.py. Requer numpy e matplotlib.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fuzzy_utils import trimf,trapmf,aggregate
OUT=Path(__file__).resolve().parent

def modelo():
    u=np.arange(0,100.01,.5)
    freq={"baixa":trapmf(u,[0,0,55,75]),"media":trimf(u,[55,75,90]),"alta":trapmf(u,[80,92,100,100])}
    nota={"baixa":trapmf(u,[0,0,45,65]),"media":trimf(u,[45,65,82]),"alta":trapmf(u,[70,85,100,100])}
    risk={"baixo":trapmf(u,[0,0,20,45]),"medio":trimf(u,[25,50,75]),"alto":trapmf(u,[55,75,100,100])}
    return u,freq,nota,risk

def inferir(frequencia,desempenho,plot=False):
    if not 0<=frequencia<=100 or not 0<=desempenho<=100: raise ValueError("As entradas devem estar entre 0 e 100%.")
    u,F,N,R=modelo()
    muF={k:float(np.interp(frequencia,u,v)) for k,v in F.items()}; muN={k:float(np.interp(desempenho,u,v)) for k,v in N.items()}
    # Base 3x3 completa; inclui E e OU. Força da disjunção é max, conjunção min.
    strengths=[
      (max(muF["baixa"],muN["baixa"]),R["alto"]),
      (min(muF["media"],muN["baixa"]),R["alto"]),
      (min(muF["baixa"],muN["media"]),R["alto"]),
      (min(muF["alta"],muN["alta"]),R["baixo"]),
      (min(muF["alta"],muN["media"]),R["medio"]),
      (min(muF["media"],muN["alta"]),R["medio"]),
      (min(muF["media"],muN["media"]),R["medio"]),
      (min(muF["alta"],muN["baixa"]),R["medio"]),
      (min(muF["baixa"],muN["alta"]),R["medio"]),
    ]
    agg,out=aggregate(u,strengths)
    if plot:
        fig,ax=plt.subplots(1,3,figsize=(13,3.7))
        for name,m in F.items():ax[0].plot(u,m,label=name)
        for name,m in N.items():ax[1].plot(u,m,label=name)
        for name,m in R.items():ax[2].plot(u,m,label=name)
        ax[2].fill_between(u,0,agg,alpha=.35,color="#4477aa");ax[2].axvline(out,color="red",ls="--",label=f"saída {out:.1f}%")
        for a,t in zip(ax,["Frequência (%)","Desempenho (%)","Risco de evasão (%)"]):a.set(title=t,xlabel="Universo (%)",ylabel="Pertinência μ");a.grid(alpha=.2);a.legend()
        fig.tight_layout();fig.savefig(OUT/"fuzzy_lab03_aula09_pertinencias.png",dpi=160);plt.close(fig)
    return out

def main():
    casos=[("Acompanhamento forte",98,92,"baixo"),("Bom desempenho geral",85,78,"baixo/médio"),("Situação intermediária",70,60,"médio"),("Alerta crítico",35,40,"alto"),("Baixa frequência, boa nota",40,90,"médio/alto")]
    for nome,f,n,esperado in casos: print(f"{nome}: frequência={f}% desempenho={n}% -> risco={inferir(f,n):.2f}% (esperado: {esperado})")
    fvals=np.linspace(0,100,41); nvals=np.linspace(0,100,41); Z=np.array([[inferir(f,n) for f in fvals] for n in nvals])
    fig=plt.figure(figsize=(8,5.5));ax=fig.add_subplot(111,projection="3d");X,Y=np.meshgrid(fvals,nvals)
    surf=ax.plot_surface(X,Y,Z,cmap="viridis",linewidth=0,antialiased=True);ax.set(xlabel="Frequência (%)",ylabel="Desempenho (%)",zlabel="Risco (%)",title="Superfície fuzzy de risco de evasão");fig.colorbar(surf,shrink=.65,label="Risco (%)");fig.tight_layout();fig.savefig(OUT/"fuzzy_lab03_aula09_superficie.png",dpi=160);plt.close(fig)
    inferir(70,60,plot=True);print("[OK] 5 cenários e dois gráficos gerados.")
if __name__=="__main__":main()
