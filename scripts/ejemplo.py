import pandas as pd
from pathlib import Path


def main():
    # Detectar raíz del proyecto automáticamente
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Datos con errores típicos (para que el cliente vea la limpieza funcionando)
    rows = [
        ["01/01/2024", "Marta López", "Bolso negro", "Bolsos", 2, "45,50", "Ana", "Tarjeta"],
        ["02-01-2024", "marta lópez", "bolso negro", "bolso", 1, "45,50 €", "Ana", "tarjeta"],
        ["03/01/2024", "Carlos Ruiz", "Mochila azul", "MOCHILAS", 1, "60.00", "Luis", "Efectivo"],
        ["03/01/2024", "Carlos Ruiz", "Mochila azul", "MOCHILAS", 1, "60.00", "Luis", "Efectivo"],  # duplicado
        ["04/01/2024", "Laura Pérez", "Cartera piel", "Carteras", 3, "1.234,56", "Ana", "Transferencia"],
        ["", "Cliente vacío", "Bolso rojo", "Bolsos", 1, "39,90", "Ana", "Tarjeta"],  # sin fecha
        ["05/01/2024", "Pedro Gómez", "Bufanda lana", "Bufandas", -1, "25,00", "Luis", "Efectivo"],  # unidades negativas
        ["06/01/2024", "Ana Martín", "Bolso negro", "BOLSO", 1, "45,50", "Ana", "Tarjeta"],
    ]

    columns = [
        "fecha",
        "cliente",
        "producto",
        "categoria",
        "unidades",
        "precio_unitario",
        "vendedor",
        "forma_pago",
    ]

    df = pd.DataFrame(rows, columns=columns)

    output_file = data_dir / "demo_input.xlsx"
    df.to_excel(output_file, index=False)

    print("✅ Archivo de ejemplo creado en:")
    print(output_file)
    print("\nAhora ejecuta:")
    print("python src/main.py")


if __name__ == "__main__":
    main()