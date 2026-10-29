# Aula 11 — Validação experimental e fechamento da AC-3

## Entrega

A pasta contém o motor Mamdani para urgência de incidentes (`src/model.py` e `src/engine.py`), a suíte de testes (`test_fuzzy_engine.py`), a implementação adicional de triagem fuzzy de UTI (`src/uti_triagem.py`) com seus testes (`test_uti_triagem.py`) e as dependências em `requirements.txt`. O pacote `src` possui inicializador para manter os imports dos testes previsíveis.

O motor de urgência utiliza impacto (0–100%), explorabilidade (0–10) e urgência (0–100%), defuzzificação pelo centroide e nove regras cobrindo a matriz 3 × 3 da Aula 10. A suíte valida limites da saída, monotonicidade em relação ao impacto, entradas inválidas e latência.

A implementação UTI segue os universos, funções de pertinência e cinco regras clínicas apresentados no roteiro. Foram implementadas as validações de frequência cardíaca em [40, 160] bpm e SpO₂ em [70, 100]%, com inferência pelo centroide. Trata-se de um exercício didático, não de ferramenta clínica; não substitui avaliação profissional ou protocolos hospitalares.

## Execução e resultados

Instalação e execução, a partir desta pasta:

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest -v test_fuzzy_engine.py test_uti_triagem.py
python3 -m pytest -s test_fuzzy_engine.py
```

### Rodada 1 — estado correto

A suíte original do motor de urgência foi executada com `pytest -v test_fuzzy_engine.py`: **4 testes passaram**. Na execução de console com `pytest -s test_fuzzy_engine.py`, também passaram **4 testes**; a medição observada foi de **1,245 ms por inferência** em 100 inferências, abaixo do SLA de 10 ms.

### Rodada 2 — erro proposital

Para validar a capacidade de detecção, foi alterado temporariamente o limite superior esperado da saída de 100 para 10. A rodada detalhada reportou **1 falha e 3 aprovações**: para o caso (impacto=50, explorabilidade=5), o resultado foi **76,6667**, acima do limite incorreto. A execução com `-s` também detectou a mesma falha. A asserção original foi restaurada em seguida; o valor alterado não ficou na versão final.

### Rodada 3 — correção e validação final

Após restaurar a asserção correta e incluir os testes clínicos, a suíte final combinada terminou com **8 testes aprovados, 0 falhas**, em **2,34 s**. A execução de console da terceira rodada mediu **1,213 ms por inferência** em 100 inferências.

| Teste | Resultado |
|---|---:|
| Saída no universo [0, 100] | aprovado |
| Monotonicidade para impacto crescente | aprovado |
| Rejeição de entradas inválidas do motor | aprovado |
| Latência (100 inferências; SLA < 10 ms/op) | aprovado |
| Paciente saudável: 75 bpm, SpO₂ 98% | aprovado; risco 11,67% |
| Queda de SpO₂: 95% versus 89% | aprovado; 35,71% versus 85,57% |
| Validação dos limites fisiológicos | aprovado |
| Combinação válida sem regra aplicável (120 bpm, SpO₂ 98%) | aprovada; erro descritivo emitido |

### Cobertura de código

Execução com `pytest-cov` (`--cov=src --cov-report=term-missing`):

| Módulo | Cobertura de linhas |
|---|---:|
| `src/engine.py` | 40% |
| `src/model.py` | 68% |
| `src/uti_triagem.py` | 79% |
| Total de `src` | **61%** |

As linhas não cobertas concentram-se nos utilitários opcionais de visualização/simulação e nos blocos de execução direta (`__main__`), que não são necessários para os testes unitários centrais.

## Observações sobre a especificação da triagem UTI

**Limite de risco em SpO₂=95%.** O roteiro pede risco estritamente menor que 35%. Porém, usando literalmente as pertinências de saída indicadas (`baixo=[0,0,35]`, `moderado=[25,50,75]`, `crítico=[65,85,100,100]`), as pertinências de SpO₂ em 95% e o método centroide, a inferência para 75 bpm resulta em **35,7067%**. Esse limite não é compatível com o próprio modelo especificado. Para não alterar silenciosamente as funções ou o método de defuzzificação, o teste final usa o limite de **36%** e documenta a diferença; a queda para SpO₂=89% produz 85,57%.

**Cobertura incompleta da base de regras.** As cinco regras fornecidas não cobrem toda combinação fisiologicamente válida. Por exemplo, 120 bpm com SpO₂ de 98% não ativa regra alguma. O helper agora converte esse caso em um `ValueError` claro, e um teste registra a limitação. Não foram inventadas regras clínicas adicionais além das cinco do enunciado; a base deve ser ampliada e validada por profissionais antes de qualquer uso além do exercício.

## Avisos da execução

O scikit-fuzzy 0.5.0 com NumPy 2.5.4 emite avisos `DeprecationWarning` internos sobre `numpy.maximum/minimum` durante a agregação. Eles não afetam os resultados: todos os testes finais passaram. Para reproduzir em outro ambiente, instale as dependências listadas em `requirements.txt`.
