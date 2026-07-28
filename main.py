
import sys


def check_python_version() -> None:
    """Verifica se a versão do Python é compatível."""
    if sys.version_info < (3, 12):
        print("❌ Erro: Python 3.12+ é necessário.")
        print(f"   Versão atual: {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)


def main() -> None:
    """Ponto de entrada principal da aplicação."""
    check_python_version()

    try:
        from terminal.ui import main as ui_main
        ui_main()
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("   Execute: pip install -r requirements.txt")
        print("   E depois: playwright install chromium")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        print(f"\n   Detalhes: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
