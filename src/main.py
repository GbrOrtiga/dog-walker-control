"""
main.py — Interface CLI do Dog Walker Control.

Execute com:
    python -m src.main
"""

from src.core import DogWalkerControl, DAYS_OF_WEEK, MAX_DAYS


def print_header():
    print("\n" + "=" * 45)
    print("       🐾  DOG WALKER CONTROL  🐾")
    print("=" * 45)


def print_menu():
    print("\n[1] Registrar passeio")
    print("[2] Listar todos os passeios")
    print("[3] Ver total a receber no mês")
    print("[4] Buscar por dono")
    print("[5] Remover registro")
    print("[6] Ver agenda da semana")
    print("[0] Sair")
    print("-" * 45)


def input_int(prompt: str) -> int | None:
    """Lê um inteiro do usuário com tratamento de erro."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("⚠  Por favor, informe um número inteiro válido.")
        return None


def choose_days() -> list[str] | None:
    """Exibe menu de dias da semana e permite selecionar até MAX_DAYS dias."""
    selected: list[str] = []

    while True:
        print(f"\nDias selecionados ({len(selected)}/{MAX_DAYS}): ", end="")
        print(", ".join(selected) if selected else "nenhum")
        print()

        # Mostra opções disponíveis
        for i, day in enumerate(DAYS_OF_WEEK, start=1):
            mark = "✓" if day in selected else " "
            print(f"  [{i}] [{mark}] {day}")

        print("\n  [0] Confirmar seleção")
        print(f"  (selecione até {MAX_DAYS} dias, digite o número para marcar/desmarcar)")

        choice = input_int("\nOpção: ")

        if choice is None:
            continue

        if choice == 0:
            if not selected:
                print("⚠  Selecione ao menos um dia.")
                continue
            return selected

        if not (1 <= choice <= len(DAYS_OF_WEEK)):
            print("⚠  Opção inválida.")
            continue

        day = DAYS_OF_WEEK[choice - 1]

        if day in selected:
            selected.remove(day)
            print(f"  ✗ '{day}' desmarcado.")
        elif len(selected) >= MAX_DAYS:
            print(f"⚠  Você já selecionou o máximo de {MAX_DAYS} dias.")
        else:
            selected.append(day)
            print(f"  ✓ '{day}' selecionado.")


def format_days(days: list[str]) -> str:
    """Formata a lista de dias de forma legível."""
    abrev = {
        "Segunda-feira": "Seg",
        "Terça-feira": "Ter",
        "Quarta-feira": "Qua",
        "Quinta-feira": "Qui",
        "Sexta-feira": "Sex",
        "Sábado": "Sáb",
        "Domingo": "Dom",
    }
    return " / ".join(abrev.get(d, d) for d in days)


def run():
    """Loop principal da aplicação CLI."""
    control = DogWalkerControl()
    print_header()
    print("📂 Dados carregados do histórico salvo.")

    while True:
        print_menu()
        choice = input("Escolha uma opção: ").strip()

        # ── [1] Registrar passeio ────────────────────────────────────
        if choice == "1":
            dog = input("Nome do cachorro: ")
            owner = input("Nome do dono: ")
            phone = input("Telefone do dono (Enter para pular): ")
            walks_per_day = input_int("Passeios por dia: ")
            if walks_per_day is None:
                continue

            days = choose_days()
            if days is None:
                continue

            try:
                record = control.add_walk(dog, owner, walks_per_day, days, phone)
                phone_info = f" | Tel: {record['phone']}" if record.get("phone") else ""
                days_fmt = format_days(record.get("days_of_week", []))
                print(
                    f"\n✅ Registrado! {record.get('dog_name', 'N/D')} — "
                    f"{days_fmt} — "
                    f"{record.get('total_walks', 0)} passeio(s)/semana — "
                    f"R$ {record.get('total', 0.0):.2f}"
                    f"{phone_info}"
                )
            except ValueError as e:
                print(f"⚠  Erro: {e}")

        # ── [2] Listar todos ─────────────────────────────────────────
        elif choice == "2":
            walks = control.list_walks()
            if not walks:
                print("\nNenhum passeio registrado ainda.")
            else:
                print(
                    f"\n{'Cachorro':<15} {'Dono':<15} {'Telefone':<14} "
                    f"{'Dias':<25} {'Pass/dia':>8} {'Total':>10}"
                )
                print("-" * 90)
                for r in walks:
                    phone = r.get("phone") or "-"
                    days_fmt = format_days(r.get("days_of_week", []))
                    walks_per_day = r.get("walks_per_day", 1)
                    total = r.get("total", 0.0)
                    print(
                        f"{r.get('dog_name', 'N/D'):<15} {r.get('owner_name', 'N/D'):<15} {phone:<14} "
                        f"{days_fmt:<25} {walks_per_day:>8} R$ {total:>8.2f}"
                    )

        # ── [3] Total a receber ──────────────────────────────────────
        elif choice == "3":
            total = control.total_revenue()
            print(f"\n💰 Total a receber no mês: R$ {total:.2f}")

        # ── [4] Buscar por dono ──────────────────────────────────────
        elif choice == "4":
            owner = input("Nome do dono: ")
            results = control.find_by_owner(owner)
            if not results:
                print(f"\nNenhum registro encontrado para '{owner}'.")
            else:
                for r in results:
                    phone = r.get("phone") or "não informado"
                    days_fmt = format_days(r.get("days_of_week", []))
                    print(
                        f"  🐕 {r.get('dog_name', 'N/D')} — {days_fmt} — "
                        f"{r.get('total_walks', 0)} passeio(s)/semana — "
                        f"R$ {r.get('total', 0.0):.2f} — Tel: {phone}"
                    )

        # ── [5] Remover registro ─────────────────────────────────────
        elif choice == "5":
            dog = input("Nome do cachorro a remover: ")
            removed = control.remove_walk(dog)
            if removed:
                print(f"✅ Registro de '{dog}' removido com sucesso.")
            else:
                print(f"⚠  Cachorro '{dog}' não encontrado.")

        # ── [6] Agenda da semana ─────────────────────────────────────
        elif choice == "6":
            by_day = control.walks_by_day()
            has_any = any(records for records in by_day.values())

            if not has_any:
                print("\nNenhum passeio registrado ainda.")
            else:
                print()
                for day, records in by_day.items():
                    if not records:
                        continue
                    
                    # Calcula totais do dia com segurança
                    total_walks_day = 0
                    total_value_day = 0
                    
                    for r in records:
                        walks_per_day = r.get("walks_per_day", 1)
                        total_walks = r.get("total_walks", walks_per_day * len(r.get("days_of_week", [])))
                        total = r.get("total", 0.0)
                        
                        total_walks_day += walks_per_day
                        total_value_day += (walks_per_day * total) / max(total_walks, 1)
                    
                    print(f"📅  {day}  ({total_walks_day} passeio(s) — R$ {total_value_day:.2f})")
                    print("    " + "-" * 52)
                    for r in records:
                        phone = r.get("phone") or "sem telefone"
                        print(
                            f"    🐕 {r.get('dog_name', 'N/D'):<15} "
                            f"Dono: {r.get('owner_name', 'N/D'):<15} "
                            f"Tel: {phone}"
                        )
                    print()

        # ── [0] Sair ─────────────────────────────────────────────────
        elif choice == "0":
            print("\nAté logo! 🐾\n")
            break

        else:
            print("⚠  Opção inválida. Tente novamente.")


if __name__ == "__main__":
    run()