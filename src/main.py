"""
main.py — Interface CLI do Dog Walker Control.

Execute com:
    python -m src.main
"""

from src.core import DogWalkerControl


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
    print("[6] Ver passeios por dia")
    print("[0] Sair")
    print("-" * 45)


def input_int(prompt: str) -> int | None:
    """Lê um inteiro do usuário com tratamento de erro."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("⚠  Por favor, informe um número inteiro válido.")
        return None


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
            walks = input_int("Quantidade de passeios: ")
            if walks is None:
                continue
            try:
                record = control.add_walk(dog, owner, walks, phone)
                phone_info = f" | Tel: {record['phone']}" if record["phone"] else ""
                print(
                    f"\n✅ Registrado! {record['dog_name']} — "
                    f"{record['walks']} passeio(s) — "
                    f"R$ {record['total']:.2f}"
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
                    f"\n{'Cachorro':<15} {'Dono':<15} {'Telefone':<15} "
                    f"{'Data':<12} {'Passeios':>8} {'Total':>10}"
                )
                print("-" * 78)
                for r in walks:
                    phone = r.get("phone") or "-"
                    date_str = r.get("date", "-")
                    print(
                        f"{r['dog_name']:<15} {r['owner_name']:<15} {phone:<15} "
                        f"{date_str:<12} {r['walks']:>8} R$ {r['total']:>8.2f}"
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
                    print(
                        f"  🐕 {r['dog_name']} — "
                        f"{r['walks']} passeio(s) — "
                        f"R$ {r['total']:.2f} — "
                        f"Tel: {phone}"
                    )

        # ── [5] Remover registro ─────────────────────────────────────
        elif choice == "5":
            dog = input("Nome do cachorro a remover: ")
            removed = control.remove_walk(dog)
            if removed:
                print(f"✅ Registro de '{dog}' removido com sucesso.")
            else:
                print(f"⚠  Cachorro '{dog}' não encontrado.")

        # ── [6] Passeios por dia ─────────────────────────────────────
        elif choice == "6":
            by_day = control.walks_by_day()
            if not by_day:
                print("\nNenhum passeio registrado ainda.")
            else:
                print(f"\n{'Data':<15} {'Passeios':>10}")
                print("-" * 27)
                for day, count in sorted(by_day.items()):
                    print(f"{day:<15} {count:>10}")

        # ── [0] Sair ─────────────────────────────────────────────────
        elif choice == "0":
            print("\nAté logo! 🐾\n")
            break

        else:
            print("⚠  Opção inválida. Tente novamente.")


if __name__ == "__main__":
    run()