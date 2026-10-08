"""Aula 08 / Lab 03 — ACO para árvore de baixa latência em 10 switches.

O enunciado não fornece matriz D nem pares críticos. Para tornar o experimento
reproduzível, D é derivada das coordenadas sintéticas fixas dos switches; o custo
é a soma das latências dos 9 enlaces da árvore. A construção usa Union-Find,
impedindo ciclos e garantindo conectividade.
Dependências: numpy, matplotlib.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

N=10; RHO=0.2; SEED=9009; OUT=Path(__file__).resolve().parent
COORD=np.array([[0,0],[1,2],[2,0],[3,1],[4,3],[5,0],[6,2],[7,0],[8,3],[9,1]], dtype=float)
D=np.zeros((N,N), dtype=float)
for i in range(N):
    for j in range(i+1,N):
        D[i,j]=D[j,i]=round(2.0+3.2*np.linalg.norm(COORD[i]-COORD[j]), 2)

class DSU:
    def __init__(self,n): self.p=list(range(n)); self.rank=[0]*n
    def find(self,x):
        while self.p[x]!=x: self.p[x]=self.p[self.p[x]]; x=self.p[x]
        return x
    def union(self,a,b):
        a,b=self.find(a),self.find(b)
        if a==b: return False
        if self.rank[a]<self.rank[b]: a,b=b,a
        self.p[b]=a
        if self.rank[a]==self.rank[b]: self.rank[a]+=1
        return True

def cost(edges): return float(sum(D[i,j] for i,j in edges))

def make_tree(tau,rng,alpha=1.0,beta=2.0):
    dsu=DSU(N); edges=[]
    while len(edges)<N-1:
        candidates=[(i,j) for i in range(N) for j in range(i+1,N) if dsu.find(i)!=dsu.find(j)]
        probs=np.array([(tau[i,j]**alpha)*(1.0/D[i,j]**beta) for i,j in candidates], dtype=float)
        probs=np.maximum(probs,1e-300); probs/=probs.sum()
        edge=candidates[int(rng.choice(len(candidates),p=probs))]
        dsu.union(*edge); edges.append(edge)
    return edges

def validar(edges):
    dsu=DSU(N)
    if len(edges)!=N-1: return False
    return all(dsu.union(*e) for e in edges) and len({dsu.find(i) for i in range(N)})==1

def random_baseline(rng, amostras=3000):
    vals=[]
    all_edges=[(i,j) for i in range(N) for j in range(i+1,N)]
    for _ in range(amostras):
        dsu=DSU(N); edges=[]
        for k in rng.permutation(len(all_edges)):
            e=all_edges[int(k)]
            if dsu.union(*e): edges.append(e)
            if len(edges)==N-1: break
        vals.append(cost(edges))
    return np.asarray(vals)

def executar(ants=70,iters=160):
    rng=np.random.default_rng(SEED); tau=np.ones((N,N),dtype=float); np.fill_diagonal(tau,0)
    best=None; best_cost=float("inf"); history=[]
    for _ in range(iters):
        colony=[make_tree(tau,rng) for _ in range(ants)]
        scored=sorted(((cost(e),e) for e in colony),key=lambda z:z[0])
        if scored[0][0]<best_cost: best_cost,best=scored[0][0],scored[0][1].copy()
        tau *= (1-RHO); np.fill_diagonal(tau,0)
        # Apenas os 20% melhores da iteração depositam feromônio.
        for c,e in scored[:max(1,ants//5)]:
            deposit=1.0/max(c,1e-12)
            for i,j in e: tau[i,j]+=deposit; tau[j,i]+=deposit
        history.append(best_cost)
    return best,best_cost,np.array(history)

def main():
    edges, val, hist=executar(); assert validar(edges)
    adjacency=np.zeros((N,N),dtype=int)
    for i,j in edges: adjacency[i,j]=adjacency[j,i]=1
    rng=np.random.default_rng(SEED+1); baseline=random_baseline(rng)
    mean_rand=float(baseline.mean()); pct=100*(mean_rand-val)/mean_rand
    print("Matriz de latências D (ms):\n",np.array2string(D,precision=1,max_line_width=140))
    print("Arestas da árvore:",sorted(edges)); print(f"Custo ACO={val:.2f} ms | custo médio aleatório={mean_rand:.2f} ms | melhor aleatório={baseline.min():.2f} ms | redução vs média aleatória={pct:.2f}%")
    print("Matriz de adjacência final:\n",adjacency)
    fig,ax=plt.subplots(1,2,figsize=(11,4.7)); ax[0].plot(hist,color="#2866a5"); ax[0].set(title="ACO — melhor latência acumulada",xlabel="Iteração",ylabel="Latência (ms)"); ax[0].grid(alpha=.25)
    im=ax[1].imshow(adjacency,cmap="Blues",vmin=0,vmax=1); ax[1].set(title="Árvore final — matriz de adjacência",xlabel="Switch",ylabel="Switch"); ax[1].set_xticks(range(N)); ax[1].set_yticks(range(N)); fig.colorbar(im,ax=ax[1],ticks=[0,1]); fig.tight_layout(); fig.savefig(OUT/"topologia_lab03_aula08.png",dpi=160)
    print("[OK] árvore conexa, acíclica, com 9 arestas; gráfico salvo.")

if __name__=="__main__": main()
