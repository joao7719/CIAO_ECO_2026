"""Utilitários didáticos, sem dependência de scikit-fuzzy, para lógica Mamdani."""
import numpy as np

def trimf(x, abc):
    x=np.asarray(x,dtype=float); a,b,c=map(float,abc)
    if not a < b < c:
        # Suporte a triângulos degenerados de ombro [a,a,c] ou [a,b,b].
        if a==b and b<c: return np.clip((c-x)/(c-b),0,1)
        if a<b and b==c: return np.clip((x-a)/(b-a),0,1)
        raise ValueError(f"Parâmetros triangulares inválidos: {abc}")
    return np.maximum(0.0,np.minimum((x-a)/(b-a),(c-x)/(c-b)))

def trapmf(x, abcd):
    x=np.asarray(x,dtype=float); a,b,c,d=map(float,abcd)
    if not (a<=b<=c<=d) or a==d: raise ValueError(f"Parâmetros trapezoidais inválidos: {abcd}")
    left=np.ones_like(x) if a==b else (x-a)/(b-a)
    right=np.ones_like(x) if c==d else (d-x)/(d-c)
    return np.clip(np.minimum(np.minimum(left,1.0),right),0.0,1.0)

def centroid(x, membership):
    x=np.asarray(x,dtype=float); m=np.asarray(membership,dtype=float)
    area=np.trapezoid(m,x)
    if area<=1e-15: raise ValueError("Saída fuzzy sem área; nenhuma regra foi ativada.")
    return float(np.trapezoid(x*m,x)/area)

def defuzzify(x,membership,method="centroid"):
    if method=="centroid": return centroid(x,membership)
    if method in ("mom","mom_mean"):
        m=np.asarray(membership,dtype=float); mx=m.max()
        if mx<=1e-15: raise ValueError("Saída fuzzy vazia.")
        return float(np.mean(np.asarray(x)[np.isclose(m,mx)]))
    if method=="som":
        m=np.asarray(membership,dtype=float); return float(np.asarray(x)[np.isclose(m,m.max())].min())
    raise ValueError("Método deve ser centroid, mom ou som.")

def aggregate(universe, consequents, method="centroid"):
    """consequents é sequência de pares (força, função_de_pertinência)."""
    agg=np.zeros_like(np.asarray(universe,dtype=float))
    for strength, mf in consequents:
        agg=np.maximum(agg,np.minimum(float(np.clip(strength,0,1)),np.asarray(mf,dtype=float)))
    return agg, defuzzify(universe,agg,method)
