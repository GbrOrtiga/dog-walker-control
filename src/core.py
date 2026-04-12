"""
core.py — Lógica de negócio do Dog Walker Control.

Responsável por:
- Registrar passeios
- Calcular valores
- Listar e remover registros
"""

PRICE_PER_WALK = 25.0  # Valor padrão por passeio em reais


class DogWalkerControl:
    """Gerencia os passeios de cachorros e os valores a receber."""

    def __init__(self, price_per_walk: float = PRICE_PER_WALK):
        if price_per_walk <= 0:
            raise ValueError("O valor por passeio deve ser positivo.")
        self.price_per_walk = price_per_walk
        self._walks: list[dict] = []

    def add_walk(self, dog_name: str, owner_name: str, walks: int) -> dict:
        """Registra passeios para um cachorro.

        Args:
            dog_name: Nome do cachorro.
            owner_name: Nome do dono.
            walks: Quantidade de passeios realizados.

        Returns:
            Dicionário com os dados do registro.

        Raises:
            ValueError: Se algum dado for inválido.
        """
        dog_name = dog_name.strip()
        owner_name = owner_name.strip()

        if not dog_name:
            raise ValueError("O nome do cachorro não pode estar vazio.")
        if not owner_name:
            raise ValueError("O nome do dono não pode estar vazio.")
        if walks <= 0:
            raise ValueError("A quantidade de passeios deve ser maior que zero.")

        total = walks * self.price_per_walk
        record = {
            "dog_name": dog_name,
            "owner_name": owner_name,
            "walks": walks,
            "total": total,
        }
        self._walks.append(record)
        return record

    def list_walks(self) -> list[dict]:
        """Retorna todos os registros de passeios."""
        return list(self._walks)

    def total_revenue(self) -> float:
        """Calcula o valor total a receber no mês."""
        return sum(r["total"] for r in self._walks)

    def remove_walk(self, dog_name: str) -> bool:
        """Remove o primeiro registro com o nome do cachorro informado.

        Args:
            dog_name: Nome do cachorro a remover.

        Returns:
            True se removido, False se não encontrado.
        """
        dog_name = dog_name.strip()
        for i, record in enumerate(self._walks):
            if record["dog_name"].lower() == dog_name.lower():
                self._walks.pop(i)
                return True
        return False

    def find_by_owner(self, owner_name: str) -> list[dict]:
        """Busca registros pelo nome do dono.

        Args:
            owner_name: Nome do dono.

        Returns:
            Lista de registros encontrados.
        """
        owner_name = owner_name.strip().lower()
        return [r for r in self._walks if r["owner_name"].lower() == owner_name]