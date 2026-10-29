"""Motor didático de inferência fuzzy para triagem de sinais vitais em UTI.

Este exemplo educacional implementa literalmente as funções de pertinência e
as cinco regras descritas no roteiro da Aula 11. Não substitui avaliação clínica,
protocolos institucionais nem decisão de profissionais de saúde.
"""

import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl


def criar_sistema_triagem_uti():
    """Constrói e retorna a simulação fuzzy Mamdani para triagem de UTI."""
    freq_cardiaca = ctrl.Antecedent(np.arange(40, 161, 1), "freq_cardiaca")
    spo2 = ctrl.Antecedent(np.arange(70, 101, 1), "spo2")
    risco = ctrl.Consequent(np.arange(0, 101, 1), "risco")
    risco.defuzzify_method = "centroid"

    # Frequência cardíaca (bpm): bradicardia, normal e taquicardia.
    freq_cardiaca["bradicardia"] = fuzzy.trimf(
        freq_cardiaca.universe, [40, 40, 60]
    )
    freq_cardiaca["normal"] = fuzzy.trimf(
        freq_cardiaca.universe, [50, 75, 100]
    )
    freq_cardiaca["taquicardia"] = fuzzy.trapmf(
        freq_cardiaca.universe, [90, 110, 160, 160]
    )

    # Saturação periférica de oxigênio (%).
    spo2["critica"] = fuzzy.trapmf(spo2.universe, [70, 70, 88, 91])
    spo2["limitrofe"] = fuzzy.trimf(spo2.universe, [89, 93, 96])
    spo2["normal"] = fuzzy.trapmf(spo2.universe, [94, 97, 100, 100])

    # Risco clínico (%).
    risco["baixo"] = fuzzy.trimf(risco.universe, [0, 0, 35])
    risco["moderado"] = fuzzy.trimf(risco.universe, [25, 50, 75])
    risco["critico"] = fuzzy.trapmf(risco.universe, [65, 85, 100, 100])

    regras = [
        # Regra de ouro: hipóxia crítica eleva o risco independentemente da FC.
        ctrl.Rule(spo2["critica"], risco["critico"], label="R1_spo2_critica"),
        ctrl.Rule(
            freq_cardiaca["bradicardia"] & spo2["limitrofe"],
            risco["critico"],
            label="R2_bradicardia_limitrofe",
        ),
        ctrl.Rule(
            freq_cardiaca["taquicardia"] & spo2["limitrofe"],
            risco["critico"],
            label="R3_taquicardia_limitrofe",
        ),
        ctrl.Rule(
            freq_cardiaca["normal"] & spo2["limitrofe"],
            risco["moderado"],
            label="R4_normal_limitrofe",
        ),
        ctrl.Rule(
            freq_cardiaca["normal"] & spo2["normal"],
            risco["baixo"],
            label="R5_normal_normal",
        ),
    ]
    sistema = ctrl.ControlSystem(regras)
    return ctrl.ControlSystemSimulation(sistema)


def avaliar_paciente(simulador, bpm, spo2_val):
    """Valida as leituras, executa a inferência e retorna o risco de 0 a 100."""
    try:
        bpm = float(bpm)
    except (TypeError, ValueError) as exc:
        raise ValueError("A frequência cardíaca deve ser numérica.") from exc
    try:
        spo2_val = float(spo2_val)
    except (TypeError, ValueError) as exc:
        raise ValueError("A SpO2 deve ser numérica.") from exc

    if not 40 <= bpm <= 160:
        raise ValueError(f"Frequência cardíaca fora do intervalo [40, 160]: {bpm}")
    if not 70 <= spo2_val <= 100:
        raise ValueError(f"SpO2 fora do intervalo [70, 100]: {spo2_val}")

    simulador.input["freq_cardiaca"] = bpm
    simulador.input["spo2"] = spo2_val
    try:
        simulador.compute()
        return float(simulador.output["risco"])
    except KeyError as exc:
        if exc.args and exc.args[0] == "risco":
            raise ValueError(
                "Nenhuma regra clínica da base especificada foi ativada "
                f"para FC={bpm:g} bpm e SpO2={spo2_val:g}%."
            ) from exc
        raise


if __name__ == "__main__":
    simulador_uti = criar_sistema_triagem_uti()
    exemplos = [(75, 98), (75, 95), (75, 89)]
    for bpm, valor_spo2 in exemplos:
        risco_calculado = avaliar_paciente(simulador_uti, bpm, valor_spo2)
        print(
            f"FC={bpm} bpm | SpO2={valor_spo2}% "
            f"-> risco fuzzy={risco_calculado:.2f}%"
        )
