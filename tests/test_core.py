"""
test_core.py — Testes automatizados para o módulo core.py.

Cobertura:
- Caminho feliz
- Múltiplos dias da semana
- Entradas inválidas
- Casos limite
- Telefone opcional
- Persistência em arquivo
- Agenda da semana
"""

import pytest
from src.core import DogWalkerControl, DAYS_OF_WEEK, MAX_DAYS

TEST_FILE = "test_data.json"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def control(tmp_path):
    """Instância limpa usando arquivo temporário para cada teste."""
    data_file = str(tmp_path / TEST_FILE)
    return DogWalkerControl(price_per_walk=25.0, data_file=data_file)


# ---------------------------------------------------------------------------
# Testes — add_walk (caminho feliz)
# ---------------------------------------------------------------------------

def test_add_walk_single_day(control):
    """Registro com 1 dia deve funcionar corretamente."""
    record = control.add_walk("Rex", "João", 2, ["Segunda-feira"])
    assert record["dog_name"] == "Rex"
    assert record["days_of_week"] == ["Segunda-feira"]
    assert record["total_walks"] == 2
    assert record["total"] == 50.0


def test_add_walk_multiple_days(control):
    """Registro com múltiplos dias deve somar os passeios corretamente."""
    days = ["Segunda-feira", "Quarta-feira", "Sexta-feira"]
    record = control.add_walk("Luna", "Maria", 1, days)
    assert record["total_walks"] == 3
    assert record["total"] == 75.0


def test_add_walk_max_days(control):
    """Registro com o máximo de dias permitidos deve funcionar."""
    days = DAYS_OF_WEEK[:MAX_DAYS]
    record = control.add_walk("Bolt", "Ana", 1, days)
    assert len(record["days_of_week"]) == MAX_DAYS


def test_add_walk_calculates_total_with_multiple_days(control):
    """Total deve ser walks_per_day * número de dias * preço."""
    record = control.add_walk("Rex", "João", 2, ["Segunda-feira", "Terça-feira"])
    assert record["total_walks"] == 4
    assert record["total"] == 100.0


def test_add_walk_persists_in_list(control):
    """O registro deve aparecer na listagem após ser adicionado."""
    control.add_walk("Luna", "Carlos", 1, ["Quarta-feira"])
    assert len(control.list_walks()) == 1


# ---------------------------------------------------------------------------
# Testes — dias da semana (entradas inválidas)
# ---------------------------------------------------------------------------

def test_add_walk_invalid_day_raises(control):
    """Dia inválido deve lançar ValueError."""
    with pytest.raises(ValueError, match="inválido"):
        control.add_walk("Rex", "João", 1, ["Funday"])


def test_add_walk_empty_days_raises(control):
    """Lista de dias vazia deve lançar ValueError."""
    with pytest.raises(ValueError, match="ao menos um dia"):
        control.add_walk("Rex", "João", 1, [])


def test_add_walk_too_many_days_raises(control):
    """Mais de MAX_DAYS dias deve lançar ValueError."""
    with pytest.raises(ValueError, match=f"{MAX_DAYS}"):
        control.add_walk("Rex", "João", 1, DAYS_OF_WEEK)


def test_add_walk_duplicate_days_raises(control):
    """Dia duplicado na lista deve lançar ValueError."""
    with pytest.raises(ValueError, match="mesmo dia"):
        control.add_walk("Rex", "João", 1, ["Segunda-feira", "Segunda-feira"])


# ---------------------------------------------------------------------------
# Testes — walks_by_day
# ---------------------------------------------------------------------------

def test_walks_by_day_empty(control):
    """Sem registros, todos os dias devem ter lista vazia."""
    by_day = control.walks_by_day()
    assert all(records == [] for records in by_day.values())


def test_walks_by_day_single_client_multiple_days(control):
    """Cliente com múltiplos dias deve aparecer em cada dia selecionado."""
    days = ["Segunda-feira", "Quarta-feira", "Sexta-feira"]
    control.add_walk("Rex", "João", 1, days)
    by_day = control.walks_by_day()
    assert len(by_day["Segunda-feira"]) == 1
    assert len(by_day["Quarta-feira"]) == 1
    assert len(by_day["Sexta-feira"]) == 1
    assert len(by_day["Terça-feira"]) == 0


def test_walks_by_day_multiple_clients_same_day(control):
    """Vários clientes no mesmo dia devem aparecer agrupados."""
    control.add_walk("Rex", "João", 1, ["Segunda-feira"])
    control.add_walk("Luna", "Maria", 2, ["Segunda-feira", "Sexta-feira"])
    by_day = control.walks_by_day()
    assert len(by_day["Segunda-feira"]) == 2
    assert len(by_day["Sexta-feira"]) == 1


def test_walks_by_day_order(control):
    """Os dias devem estar na ordem correta da semana."""
    by_day = control.walks_by_day()
    assert list(by_day.keys()) == DAYS_OF_WEEK


# ---------------------------------------------------------------------------
# Testes — telefone opcional
# ---------------------------------------------------------------------------

def test_add_walk_with_phone(control):
    record = control.add_walk("Rex", "João", 1, ["Segunda-feira"], phone="11999999999")
    assert record["phone"] == "11999999999"


def test_add_walk_without_phone(control):
    record = control.add_walk("Rex", "João", 1, ["Segunda-feira"])
    assert record["phone"] == ""


# ---------------------------------------------------------------------------
# Testes — persistência
# ---------------------------------------------------------------------------

def test_data_persists_after_reload(tmp_path):
    """Dados salvos devem ser carregados em nova instância."""
    data_file = str(tmp_path / TEST_FILE)
    c1 = DogWalkerControl(data_file=data_file)
    c1.add_walk("Rex", "João", 2, ["Terça-feira", "Quinta-feira"])

    c2 = DogWalkerControl(data_file=data_file)
    assert len(c2.list_walks()) == 1
    assert c2.list_walks()[0]["days_of_week"] == ["Terça-feira", "Quinta-feira"]


def test_removal_persists_after_reload(tmp_path):
    """Remoção deve ser persistida no arquivo."""
    data_file = str(tmp_path / TEST_FILE)
    c1 = DogWalkerControl(data_file=data_file)
    c1.add_walk("Rex", "João", 1, ["Segunda-feira"])
    c1.remove_walk("Rex")

    c2 = DogWalkerControl(data_file=data_file)
    assert len(c2.list_walks()) == 0


# ---------------------------------------------------------------------------
# Testes — entradas inválidas gerais
# ---------------------------------------------------------------------------

def test_add_walk_raises_on_empty_dog_name(control):
    with pytest.raises(ValueError, match="cachorro"):
        control.add_walk("", "João", 1, ["Segunda-feira"])


def test_add_walk_raises_on_empty_owner_name(control):
    with pytest.raises(ValueError, match="dono"):
        control.add_walk("Rex", "  ", 1, ["Segunda-feira"])


def test_add_walk_raises_on_zero_walks(control):
    with pytest.raises(ValueError, match="maior que zero"):
        control.add_walk("Rex", "João", 0, ["Segunda-feira"])


def test_add_walk_raises_on_negative_walks(control):
    with pytest.raises(ValueError, match="maior que zero"):
        control.add_walk("Rex", "João", -1, ["Segunda-feira"])


def test_invalid_price_raises_on_init():
    with pytest.raises(ValueError):
        DogWalkerControl(price_per_walk=0)


# ---------------------------------------------------------------------------
# Testes — total_revenue e remove
# ---------------------------------------------------------------------------

def test_total_revenue_empty(control):
    assert control.total_revenue() == 0.0


def test_total_revenue_multiple_records(control):
    control.add_walk("Rex", "João", 1, ["Segunda-feira", "Quarta-feira"])  # 50.0
    control.add_walk("Luna", "Maria", 2, ["Sexta-feira"])                  # 50.0
    assert control.total_revenue() == 100.0


def test_remove_walk_existing(control):
    control.add_walk("Rex", "João", 1, ["Segunda-feira"])
    assert control.remove_walk("Rex") is True
    assert len(control.list_walks()) == 0


def test_remove_walk_nonexistent(control):
    assert control.remove_walk("Fantasma") is False


def test_remove_walk_case_insensitive(control):
    control.add_walk("Rex", "João", 1, ["Segunda-feira"])
    assert control.remove_walk("rex") is True


# ---------------------------------------------------------------------------
# Testes — find_by_owner
# ---------------------------------------------------------------------------

def test_find_by_owner_returns_correct_records(control):
    control.add_walk("Rex", "João", 1, ["Segunda-feira"])
    control.add_walk("Luna", "Maria", 1, ["Terça-feira"])
    results = control.find_by_owner("João")
    assert len(results) == 1
    assert results[0]["dog_name"] == "Rex"


def test_find_by_owner_not_found(control):
    assert control.find_by_owner("Ninguém") == []