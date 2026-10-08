"""Aula 09 / Lab 01 — controle fuzzy de ventilador (Mamdani, centroide).
Execução: python3 lab01_aula09.py. Requer numpy e matplotlib.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fuzzy_utils import trimf, trapmf, aggregate
OUT=Path(__file__).resolve().parent

def memberships():
    t=np.arange(0,40.01,.1); v=np.arange(0,100.01,.25)
    temp={"frio":trapmf(t,[0,0,15,25]),"morno":trimf(t,[15,25,35]),"quente":trapmf(t,[25,35,40,40])}
    fan={"baixa":trimf(v,[0,0,50]),"media":trimf(v,[0,50,100]),"alta":trimf(v,[50,100,100])}
    return t,v,temp,fan

def controlar(valor, plot=False):
    t,v,temp,fan=memberships()
    mu={name:float(np.interp(valor,t,mf)) for name,mf in temp.items()}
    agg,out=aggregate(v,[(mu["frio"],fan["baixa"]),(mu["morno"],fan["media"]),(mu["quente"],fan["alta"])])
    if plot:
        fig,ax=plt.subplots(1,2,figsize=(10,4));
        for name,mf in temp.items(): ax[0].plot(t,mf,label=name)
        for name,mf in fan.items(): ax[1].plot(v,mf,label=name)
        ax[0].set(title="Temperatura: pertinências",xlabel="°C",ylabel="μ"); ax[1].plot(v,agg,color="black",lw=2,label="agregada"); ax[1].axvline(out,color="red",ls="--",label=f"centroide={out:.1f}%"); ax[1].set(title=f"Velocidade para {valor:g} °C",xlabel="Velocidade (%)",ylabel="μ")
        for a in ax:a.grid(alpha=.2);a.legend()
        fig.tight_layout();fig.savefig(OUT/"fuzzy_lab01_aula09.png",dpi=160);plt.close(fig)
    return out

def main():
    for temp in (10,20,25,30,38): print(f"{temp:>4} °C -> ventilador a {controlar(temp):.2f}%")
    controlar(25,plot=True); print("[OK] gráfico de pertinência e saída salvo.")
if __name__=="__main__":main()
