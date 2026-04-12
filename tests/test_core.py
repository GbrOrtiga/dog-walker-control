"""
test_core.py — Testes automatizados para o módulo core.py.

Cobertura:
- Caminho feliz (uso correto)
- Entradas inválidas
- Casos limite
- Telefone opcional
- Dia da semana
- Persistência em arquivo
- Agenda da semana
"""

import pytest
from src.core import DogWalkerControl, DAYS_OF_WEEK

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

def test_add_walk_returns_correct_record(control):
    """Deve retornar registro com os dados informados."""
    record = control.add_walk("Rex", "João", 3, "Segunda-feira")
    assert record["dog_name"] == "Rex"
    assert record["owner_name"] == "João"
    assert record["walks"] == 3
    assert record["total"] == 75.0
    assert record["day_of_week"] == "Segunda-feira"


def test_add_walk_calculates_total_correctly(control):
    """Deve calcular o total multiplicando passeios pelo preço."""
    record = control.add_walk("Bolinha", "Maria", 5, "Sexta-feira")
    assert record["total"] == 125.0


def test_add_walk_persists_in_list(control):
    """O registro deve aparecer na listagem após ser adicionado."""
    control.add_walk("Luna", "Carlos", 2, "Quarta-feira")
    walks = control.list_walks()
    assert len(walks) == 1
    assert walks[0]["dog_name"] == "Luna"


def test_add_walk_saves_date(control):
    """O registro deve conter a data de hoje."""
    from datetime import date
    record = control.add_walk("Rex", "João", 1, "Terça-feira")
    assert record["date"] == date.today().isoformat()


# ---------------------------------------------------------------------------
# Testes — dia da semana
# ---------------------------------------------------------------------------

def test_add_walk_saves_day_of_week(control):
    """Deve salvar o dia da semana informado."""
    record = control.add_walk("Rex", "João", 2, "Sábado")
    assert record["day_of_week"] == "Sábado"


def test_add_walk_invalid_day_raises(control):
    """Dia da semana inválido deve lançar ValueError."""
    with pytest.raises(ValueError, match="inválido"):
        control.add_walk("Rex", "João", 2, "Funday")


def test_all_days_are_valid(control):
    """Todos os dias da semana da lista devem ser aceitos."""
    for i, day in enumerate(DAYS_OF_WEEK):
        control.add_walk(f"Dog{i}", "Dono", 1, day)
    assert len(control.list_walks()) == len(DAYS_OF_WEEK)


# ---------------------------------------------------------------------------
# Testes — walks_by_day
# ---------------------------------------------------------------------------

def test_walks_by_day_empty(control):
    """Sem registros, todos os dias devem ter lista vazia."""
    by_day = control.walks_by_day()
    assert all(records == [] for records in by_day.values())


def test_walks_by_day_groups_correctly(control):
    """Passeios devem aparecer no dia correto."""
    control.add_walk("Rex", "João", 2, "Segunda-feira")
    control.add_walk("Luna", "Maria", 3, "Segunda-feira")
    control.add_walk("Bolt", "Ana", 1, "Sexta-feira")
    by_day = control.walks_by_day()
    assert len(by_day["Segunda-feira"]) == 2
    assert len(by_day["Sexta-feira"]) == 1
    assert len(by_day["Terça-feira"]) == 0


def test_walks_by_day_order(control):
    """Os dias devem estar na ordem correta da semana."""
    by_day = control.walks_by_day()
    assert list(by_day.keys()) == DAYS_OF_WEEK


# ---------------------------------------------------------------------------
# Testes — telefone opcional
# ---------------------------------------------------------------------------

def test_add_walk_with_phone(control):
    """Deve salvar o telefone quando informado."""
    record = control.add_walk("Rex", "João", 2, "Segunda-feira", phone="11999999999")
    assert record["phone"] == "11999999999"


def test_add_walk_without_phone(control):
    """Telefone deve ser string vazia quando não informado."""
    record = control.add_walk("Rex", "João", 2, "Segunda-feira")
    assert record["phone"] == ""


# ---------------------------------------------------------------------------
# Testes — persistência em arquivo
# ---------------------------------------------------------------------------

def test_data_persists_after_reload(tmp_path):
    """Dados salvos devem ser carregados em nova instância."""
    data_file = str(tmp_path / TEST_FILE)
    c1 = DogWalkerControl(data_file=data_file)
    c1.add_walk("Rex", "João", 3, "Terça-feira")

    c2 = DogWalkerControl(data_file=data_file)
    assert len(c2.list_walks()) == 1
    assert c2.list_walks()[0]["day_of_week"] == "Terça-feira"


def test_removal_persists_after_reload(tmp_path):
    """Remoção deve ser persistida no arquivo."""
    data_file = str(tmp_path / TEST_FILE)
    c1 = DogWalkerControl(data_file=data_file)
    c1.add_walk("Rex", "João", 3, "Segunda-feira")
    c1.remove_walk("Rex")

    c2 = DogWalkerControl(data_file=data_file)
    assert len(c2.list_walks()) == 0


# ---------------------------------------------------------------------------
# Testes — entradas inválidas
# ---------------------------------------------------------------------------

def test_add_walk_raises_on_empty_dog_name(control):
    with pytest.raises(ValueError, match="cachorro"):
        control.add_walk("", "João", 3, "Segunda-feira")


def test_add_walk_raises_on_empty_owner_name(control):
    with pytest.raises(ValueError, match="dono"):
        control.add_walk("Rex", "  ", 3, "Segunda-feira")


def test_add_walk_raises_on_zero_walks(control):
    with pytest.raises(ValueError, match="maior que zero"):
        control.add_walk("Rex", "João", 0, "Segunda-feira")


def test_add_walk_raises_on_negative_walks(control):
    with pytest.raises(ValueError, match="maior que zero"):
        control.add_walk("Rex", "João", -1, "Segunda-feira")


def test_invalid_price_raises_on_init():
    with pytest.raises(ValueError):
        DogWalkerControl(price_per_walk=0)


# ---------------------------------------------------------------------------
# Testes — total_revenue
# ---------------------------------------------------------------------------

def test_total_revenue_empty(control):
    assert control.total_revenue() == 0.0


def test_total_revenue_multiple_records(control):
    control.add_walk("Rex", "João", 4, "Segunda-feira")
    control.add_walk("Luna", "Maria", 2, "Quarta-feira")
    assert control.total_revenue() == 150.0


# ---------------------------------------------------------------------------
# Testes — remove_walk
# ---------------------------------------------------------------------------

def test_remove_walk_existing(control):
    control.add_walk("Rex", "João", 2, "Segunda-feira")
    assert control.remove_walk("Rex") is True
    assert len(control.list_walks()) == 0


def test_remove_walk_nonexistent(control):
    assert control.remove_walk("Fantasma") is False


def test_remove_walk_case_insensitive(control):
    control.add_walk("Rex", "João", 2, "Segunda-feira")
    assert control.remove_walk("rex") is True


# ---------------------------------------------------------------------------
# Testes — find_by_owner
# ---------------------------------------------------------------------------

def test_find_by_owner_returns_correct_records(control):
    control.add_walk("Rex", "João", 2, "Segunda-feira")
    control.add_walk("Luna", "Maria", 3, "Terça-feira")
    results = control.find_by_owner("João")
    assert len(results) == 1
    assert results[0]["dog_name"] == "Rex"


def test_find_by_owner_not_found(control):
    assert control.find_by_owner("Ninguém") == []