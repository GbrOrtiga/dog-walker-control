"""
test_core.py — Testes automatizados para o módulo core.py.

Cobertura:
- Caminho feliz (uso correto)
- Entradas inválidas
- Casos limite
- Telefone opcional
- Persistência em arquivo
- Passeios por dia
"""


import pytest
from src.core import DogWalkerControl

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
    record = control.add_walk("Rex", "João", 3)
    assert record["dog_name"] == "Rex"
    assert record["owner_name"] == "João"
    assert record["walks"] == 3
    assert record["total"] == 75.0


def test_add_walk_calculates_total_correctly(control):
    """Deve calcular o total multiplicando passeios pelo preço."""
    record = control.add_walk("Bolinha", "Maria", 5)
    assert record["total"] == 125.0


def test_add_walk_persists_in_list(control):
    """O registro deve aparecer na listagem após ser adicionado."""
    control.add_walk("Luna", "Carlos", 2)
    walks = control.list_walks()
    assert len(walks) == 1
    assert walks[0]["dog_name"] == "Luna"


def test_add_walk_saves_date(control):
    """O registro deve conter a data de hoje."""
    from datetime import date
    record = control.add_walk("Rex", "João", 1)
    assert record["date"] == date.today().isoformat()


# ---------------------------------------------------------------------------
# Testes — telefone opcional
# ---------------------------------------------------------------------------

def test_add_walk_with_phone(control):
    """Deve salvar o telefone quando informado."""
    record = control.add_walk("Rex", "João", 2, phone="11999999999")
    assert record["phone"] == "11999999999"


def test_add_walk_without_phone(control):
    """Telefone deve ser string vazia quando não informado."""
    record = control.add_walk("Rex", "João", 2)
    assert record["phone"] == ""


# ---------------------------------------------------------------------------
# Testes — persistência em arquivo
# ---------------------------------------------------------------------------

def test_data_persists_after_reload(tmp_path):
    """Dados salvos devem ser carregados em nova instância."""
    data_file = str(tmp_path / TEST_FILE)
    c1 = DogWalkerControl(data_file=data_file)
    c1.add_walk("Rex", "João", 3)

    c2 = DogWalkerControl(data_file=data_file)
    assert len(c2.list_walks()) == 1
    assert c2.list_walks()[0]["dog_name"] == "Rex"


def test_removal_persists_after_reload(tmp_path):
    """Remoção deve ser persistida no arquivo."""
    data_file = str(tmp_path / TEST_FILE)
    c1 = DogWalkerControl(data_file=data_file)
    c1.add_walk("Rex", "João", 3)
    c1.remove_walk("Rex")

    c2 = DogWalkerControl(data_file=data_file)
    assert len(c2.list_walks()) == 0


# ---------------------------------------------------------------------------
# Testes — add_walk (entradas inválidas)
# ---------------------------------------------------------------------------

def test_add_walk_raises_on_empty_dog_name(control):
    """Nome de cachorro vazio deve lançar ValueError."""
    with pytest.raises(ValueError, match="cachorro"):
        control.add_walk("", "João", 3)


def test_add_walk_raises_on_empty_owner_name(control):
    """Nome de dono vazio deve lançar ValueError."""
    with pytest.raises(ValueError, match="dono"):
        control.add_walk("Rex", "  ", 3)


def test_add_walk_raises_on_zero_walks(control):
    """Zero passeios deve lançar ValueError."""
    with pytest.raises(ValueError, match="maior que zero"):
        control.add_walk("Rex", "João", 0)


def test_add_walk_raises_on_negative_walks(control):
    """Quantidade negativa de passeios deve lançar ValueError."""
    with pytest.raises(ValueError, match="maior que zero"):
        control.add_walk("Rex", "João", -1)


def test_invalid_price_raises_on_init():
    """Preço por passeio inválido deve lançar ValueError na criação."""
    with pytest.raises(ValueError):
        DogWalkerControl(price_per_walk=0)


# ---------------------------------------------------------------------------
# Testes — total_revenue
# ---------------------------------------------------------------------------

def test_total_revenue_empty(control):
    """Sem registros, o total deve ser zero."""
    assert control.total_revenue() == 0.0


def test_total_revenue_multiple_records(control):
    """Total deve somar todos os registros corretamente."""
    control.add_walk("Rex", "João", 4)    # 100.0
    control.add_walk("Luna", "Maria", 2)  # 50.0
    assert control.total_revenue() == 150.0


# ---------------------------------------------------------------------------
# Testes — remove_walk
# ---------------------------------------------------------------------------

def test_remove_walk_existing(control):
    """Remover um cachorro existente deve retornar True."""
    control.add_walk("Rex", "João", 2)
    assert control.remove_walk("Rex") is True
    assert len(control.list_walks()) == 0


def test_remove_walk_nonexistent(control):
    """Remover um cachorro inexistente deve retornar False."""
    assert control.remove_walk("Fantasma") is False


def test_remove_walk_case_insensitive(control):
    """A remoção deve ser insensível a maiúsculas/minúsculas."""
    control.add_walk("Rex", "João", 2)
    assert control.remove_walk("rex") is True


# ---------------------------------------------------------------------------
# Testes — find_by_owner
# ---------------------------------------------------------------------------

def test_find_by_owner_returns_correct_records(control):
    """Deve retornar apenas registros do dono informado."""
    control.add_walk("Rex", "João", 2)
    control.add_walk("Luna", "Maria", 3)
    results = control.find_by_owner("João")
    assert len(results) == 1
    assert results[0]["dog_name"] == "Rex"


def test_find_by_owner_not_found(control):
    """Dono inexistente deve retornar lista vazia."""
    assert control.find_by_owner("Ninguém") == []


# ---------------------------------------------------------------------------
# Testes — walks_by_day
# ---------------------------------------------------------------------------

def test_walks_by_day_empty(control):
    """Sem registros, walks_by_day deve retornar dicionário vazio."""
    assert control.walks_by_day() == {}


def test_walks_by_day_groups_correctly(control):
    """Passeios do mesmo dia devem ser somados."""
    from datetime import date
    today = date.today().isoformat()
    control.add_walk("Rex", "João", 2)
    control.add_walk("Luna", "Maria", 3)
    by_day = control.walks_by_day()
    assert by_day[today] == 5