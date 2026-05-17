"""
Teste de integração com a API pública ViaCEP (https://viacep.com.br).

Cobre dois cenários:
  1. CEP válido  → resposta real da API com os campos esperados
  2. CEP inválido → campo "erro" presente na resposta

Execute com:
    pytest tests/test_viacep.py -v
"""

import pytest
import requests
from unittest.mock import patch, MagicMock

VIACEP_URL = "https://viacep.com.br/ws/{cep}/json/"


# ══════════════════════════════════════════════════════════════
# Funções que seriam chamadas pelo backend (src/web.py)
# ══════════════════════════════════════════════════════════════

def buscar_endereco_por_cep(cep: str) -> dict:
    """Consulta o ViaCEP e retorna os dados do endereço.

    Args:
        cep: CEP com 8 dígitos (somente números).

    Returns:
        dict com os dados do endereço ou {"erro": True} se não encontrado.

    Raises:
        ValueError: se o CEP não tiver exatamente 8 dígitos numéricos.
        requests.RequestException: em caso de falha de rede.
    """
    cep = cep.replace("-", "").strip()

    if len(cep) != 8 or not cep.isdigit():
        raise ValueError(f"CEP inválido: '{cep}'. Deve conter exatamente 8 dígitos.")

    response = requests.get(VIACEP_URL.format(cep=cep), timeout=5)
    response.raise_for_status()
    return response.json()


def formatar_endereco(dados: dict) -> str:
    """Formata os dados do ViaCEP em uma string legível."""
    if dados.get("erro"):
        return ""
    partes = [
        dados.get("logradouro", ""),
        dados.get("bairro", ""),
        dados.get("localidade", ""),
        dados.get("uf", ""),
    ]
    return ", ".join(p for p in partes if p)


# ══════════════════════════════════════════════════════════════
# Testes com mock (sem depender de conexão real)
# ══════════════════════════════════════════════════════════════

class TestViaCepMock:
    """Testes de integração usando mock da API ViaCEP."""

    def test_cep_valido_retorna_campos_esperados(self):
        """CEP válido deve retornar um dict com os campos de endereço."""
        dados_mock = {
            "cep": "01310-100",
            "logradouro": "Avenida Paulista",
            "bairro": "Bela Vista",
            "localidade": "São Paulo",
            "uf": "SP",
            "ibge": "3550308",
            "ddd": "11",
        }

        mock_response = MagicMock()
        mock_response.json.return_value = dados_mock
        mock_response.raise_for_status = MagicMock()

        with patch("requests.get", return_value=mock_response) as mock_get:
            resultado = buscar_endereco_por_cep("01310100")

        mock_get.assert_called_once_with(
            "https://viacep.com.br/ws/01310100/json/", timeout=5
        )
        assert resultado["localidade"] == "São Paulo"
        assert resultado["uf"] == "SP"
        assert resultado["logradouro"] == "Avenida Paulista"
        assert "cep" in resultado

    def test_cep_invalido_retorna_erro(self):
        """CEP inexistente deve retornar campo 'erro' igual a True."""
        dados_mock = {"erro": True}

        mock_response = MagicMock()
        mock_response.json.return_value = dados_mock
        mock_response.raise_for_status = MagicMock()

        with patch("requests.get", return_value=mock_response):
            resultado = buscar_endereco_por_cep("00000000")

        assert resultado.get("erro") is True

    def test_cep_com_hifen_e_normalizado(self):
        """CEP formatado com hífen deve ser aceito e normalizado."""
        dados_mock = {
            "localidade": "Curitiba",
            "uf": "PR",
            "logradouro": "Rua XV de Novembro",
            "bairro": "Centro",
        }

        mock_response = MagicMock()
        mock_response.json.return_value = dados_mock
        mock_response.raise_for_status = MagicMock()

        with patch("requests.get", return_value=mock_response) as mock_get:
            resultado = buscar_endereco_por_cep("80020-310")

        # Verifica que a URL usada não contém hífen
        url_chamada = mock_get.call_args[0][0]
        assert "-" not in url_chamada
        assert resultado["localidade"] == "Curitiba"

    def test_cep_com_menos_de_8_digitos_levanta_excecao(self):
        """CEP com menos de 8 dígitos deve levantar ValueError."""
        with pytest.raises(ValueError, match="CEP inválido"):
            buscar_endereco_por_cep("1234")

    def test_cep_com_letras_levanta_excecao(self):
        """CEP com letras deve levantar ValueError."""
        with pytest.raises(ValueError, match="CEP inválido"):
            buscar_endereco_por_cep("ABCDEFGH")

    def test_formatar_endereco_cep_valido(self):
        """formatar_endereco deve montar string legível a partir dos dados."""
        dados = {
            "logradouro": "Avenida Paulista",
            "bairro": "Bela Vista",
            "localidade": "São Paulo",
            "uf": "SP",
        }
        resultado = formatar_endereco(dados)
        assert "São Paulo" in resultado
        assert "SP" in resultado
        assert "Avenida Paulista" in resultado

    def test_formatar_endereco_cep_invalido_retorna_vazio(self):
        """formatar_endereco deve retornar string vazia para CEP não encontrado."""
        dados = {"erro": True}
        resultado = formatar_endereco(dados)
        assert resultado == ""

    def test_erro_de_rede_levanta_excecao(self):
        """Falha de conexão deve propagar requests.RequestException."""
        with patch("requests.get", side_effect=requests.ConnectionError("sem conexão")):
            with pytest.raises(requests.RequestException):
                buscar_endereco_por_cep("01310100")


# ══════════════════════════════════════════════════════════════
# Teste real (opcional — marcado com skip por padrão)
# Para rodar: pytest tests/test_viacep.py -v -m real
# ══════════════════════════════════════════════════════════════

@pytest.mark.real
def test_integracao_real_viacep():
    """Teste real contra a API ViaCEP (requer conexão com a internet).

    Execute apenas manualmente:
        pytest tests/test_viacep.py -v -m real
    """
    resultado = buscar_endereco_por_cep("01310100")
    assert "localidade" in resultado
    assert resultado["uf"] == "SP"
    assert not resultado.get("erro")
