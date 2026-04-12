"""
main.py — Interface CLI do Dog Walker Control.

Execute com:
    python -m src.main
    ou
    python src/main.py
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

    while True:
        print_menu()
        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            dog = input("Nome do cachorro: ")
            owner = input("Nome do dono: ")
            walks = input_int("Quantidade de passeios: ")
            if walks is None:
                continue
            try:
                record = control.add_walk(dog, owner, walks)
                print(
                    f"\n✅ Registrado! {record['dog_name']} — "
                    f"{record['walks']} passeio(s) — "
                    f"R$ {record['total']:.2f}"
                )
            except ValueError as e:
                print(f"⚠  Erro: {e}")

        elif choice == "2":
            walks = control.list_walks()
            if not walks:
                print("\nNenhum passeio registrado ainda.")
            else:
                print(f"\n{'Cachorro':<20} {'Dono':<20} {'Passeios':>8} {'Total':>10}")
                print("-" * 62)
                for r in walks:
                    print(
                        f"{r['dog_name']:<20} {r['owner_name']:<20} "
                        f"{r['walks']:>8} R$ {r['total']:>8.2f}"
                    )

        elif choice == "3":
            total = control.total_revenue()
            print(f"\n💰 Total a receber no mês: R$ {total:.2f}")

        elif choice == "4":
            owner = input("Nome do dono: ")
            results = control.find_by_owner(owner)
            if not results:
                print(f"\nNenhum registro encontrado para '{owner}'.")
            else:
                for r in results:
                    print(
                        f"  🐕 {r['dog_name']} — "
                        f"{r['walks']} passeio(s) — R$ {r['total']:.2f}"
                    )

        elif choice == "5":
            dog = input("Nome do cachorro a remover: ")
            removed = control.remove_walk(dog)
            if removed:
                print(f"✅ Registro de '{dog}' removido com sucesso.")
            else:
                print(f"⚠  Cachorro '{dog}' não encontrado.")

        elif choice == "0":
            print("\nAté logo! 🐾\n")
            break

        else:
            print("⚠  Opção inválida. Tente novamente.")


if __name__ == "__main__":
    run()