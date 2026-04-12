"""
core.py — Lógica de negócio do Dog Walker Control.

Responsável por:
- Registrar passeios (com telefone opcional e até 5 dias da semana)
- Calcular valores
- Listar e remover registros
- Persistir dados em arquivo JSON
- Exibir passeios agrupados por dia da semana
"""

import json
import os
from datetime import date

PRICE_PER_WALK = 25.0
DATA_FILE = "data.json"

DAYS_OF_WEEK = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo",
]

MAX_DAYS = 5


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
        walks_per_day: int,
        days_of_week: list[str],
        phone: str = "",
    ) -> dict:
        """Registra passeios para um cachorro em múltiplos dias da semana.

        Args:
            dog_name: Nome do cachorro.
            owner_name: Nome do dono.
            walks_per_day: Quantidade de passeios por dia.
            days_of_week: Lista de dias da semana (1 a 5 dias).
            phone: Telefone do dono (opcional).

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
        if walks_per_day <= 0:
            raise ValueError("A quantidade de passeios deve ser maior que zero.")
        if not days_of_week:
            raise ValueError("Selecione ao menos um dia da semana.")
        if len(days_of_week) > MAX_DAYS:
            raise ValueError(f"Selecione no máximo {MAX_DAYS} dias.")
        for day in days_of_week:
            if day not in DAYS_OF_WEEK:
                raise ValueError(f"Dia da semana inválido: {day}")
        if len(days_of_week) != len(set(days_of_week)):
            raise ValueError("Não é permitido selecionar o mesmo dia mais de uma vez.")

        total_walks = walks_per_day * len(days_of_week)
        total = total_walks * self.price_per_walk

        record = {
            "dog_name": dog_name,
            "owner_name": owner_name,
            "phone": phone,
            "walks_per_day": walks_per_day,
            "days_of_week": days_of_week,
            "total_walks": total_walks,
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

    def walks_by_day(self) -> dict[str, list[dict]]:
        """Retorna registros agrupados por dia da semana, em ordem."""
        result: dict[str, list[dict]] = {day: [] for day in DAYS_OF_WEEK}
        for r in self._walks:
            for day in r.get("days_of_week", []):
                if day in result:
                    result[day].append(r)
        return result