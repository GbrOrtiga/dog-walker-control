"""
core.py — Lógica de negócio do Dog Walker Control.

Responsável por:
- Registrar passeios (com telefone opcional)
- Calcular valores
- Listar e remover registros
- Persistir dados em arquivo JSON
- Exibir passeios por dia
"""

import json
import os
from datetime import date

PRICE_PER_WALK = 25.0
DATA_FILE = "data.json"


class DogWalkerControl:
    """Gerencia os passeios de cachorros e os valores a receber."""

    def __init__(self, price_per_walk: float = PRICE_PER_WALK, data_file: str = DATA_FILE):
        if price_per_walk <= 0:
            raise ValueError("O valor por passeio deve ser positivo.")
        self.price_per_walk = price_per_walk
        self.data_file = data_file
        self._walks: list[dict] = []
        self._load()

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------

    def _load(self):
        """Carrega os dados do arquivo JSON, se existir."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self._walks = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._walks = []

    def _save(self):
        """Salva os dados atuais no arquivo JSON."""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self._walks, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # Operações
    # ------------------------------------------------------------------

    def add_walk(
        self,
        dog_name: str,
        owner_name: str,
        walks: int,
        phone: str = "",
    ) -> dict:
        """Registra passeios para um cachorro.

        Args:
            dog_name: Nome do cachorro.
            owner_name: Nome do dono.
            walks: Quantidade de passeios realizados.
            phone: Telefone do dono (opcional, pressione Enter para pular).

        Returns:
            Dicionário com os dados do registro.
        """
        dog_name = dog_name.strip()
        owner_name = owner_name.strip()
        phone = phone.strip()

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
            "phone": phone,
            "walks": walks,
            "total": total,
            "date": date.today().isoformat(),
        }
        self._walks.append(record)
        self._save()
        return record

    def list_walks(self) -> list[dict]:
        """Retorna todos os registros de passeios."""
        return list(self._walks)

    def total_revenue(self) -> float:
        """Calcula o valor total a receber no mês."""
        return sum(r["total"] for r in self._walks)

    def remove_walk(self, dog_name: str) -> bool:
        """Remove o primeiro registro com o nome do cachorro informado."""
        dog_name = dog_name.strip()
        for i, record in enumerate(self._walks):
            if record["dog_name"].lower() == dog_name.lower():
                self._walks.pop(i)
                self._save()
                return True
        return False

    def find_by_owner(self, owner_name: str) -> list[dict]:
        """Busca registros pelo nome do dono."""
        owner_name = owner_name.strip().lower()
        return [r for r in self._walks if r["owner_name"].lower() == owner_name]

    def walks_by_day(self) -> dict[str, int]:
        """Retorna um dicionário com a quantidade de passeios por data."""
        result: dict[str, int] = {}
        for r in self._walks:
            day = r.get("date", "sem data")
            result[day] = result.get(day, 0) + r["walks"]
        return result