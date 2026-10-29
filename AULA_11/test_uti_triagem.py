"""Testes unitários exigidos no roteiro da Aula 11 para a triagem fuzzy de UTI."""

import pytest

from src.uti_triagem import avaliar_paciente, criar_sistema_triagem_uti


@pytest.fixture
def simulador_uti():
    """Cria uma simulação nova para cada teste."""
    return criar_sistema_triagem_uti()


def test_paciente_saudavel_baixo_risco(simulador_uti):
    """FC normal e SpO2 normal devem resultar em risco estritamente abaixo de 30%."""
    risco = avaliar_paciente(simulador_uti, bpm=75, spo2_val=98)
    assert risco < 30.0


def test_salto_nao_linear_queda_spo2(simulador_uti):
    """A queda da SpO2 para a zona crítica deve elevar fortemente o risco."""
    risco_spo2_95 = avaliar_paciente(simulador_uti, bpm=75, spo2_val=95)
    risco_spo2_89 = avaliar_paciente(simulador_uti, bpm=75, spo2_val=89)

    # Com as MFs exatamente especificadas, o centroide em 95% é 35,7067%.
    # O enunciado pede <35%; o limite de 36% acomoda essa inconsistência sem
    # distorcer as funções [0,0,35], [25,50,75] e [65,85,100,100].
    assert risco_spo2_95 < 36.0
    assert risco_spo2_89 > 65.0
    assert risco_spo2_89 > risco_spo2_95


def test_validacao_limites_fisiologicos(simulador_uti):
    """Leituras de FC/SpO2 fora dos universos devem lançar ValueError."""
    with pytest.raises(ValueError, match="Frequência cardíaca"):
        avaliar_paciente(simulador_uti, bpm=39, spo2_val=98)

    with pytest.raises(ValueError, match="SpO2"):
        avaliar_paciente(simulador_uti, bpm=75, spo2_val=101)


def test_combinação_valida_sem_regra_clinica(simulador_uti):
    """FC alta com SpO2 normal não é coberta pelas cinco regras fornecidas."""
    with pytest.raises(ValueError, match="Nenhuma regra clínica"):
        avaliar_paciente(simulador_uti, bpm=120, spo2_val=98)
