from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def generate_charts(df: pd.DataFrame, out_dir: str | Path) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    charts = {}

    # Asegurar datetime
    dfx = df.copy()
    dfx["fecha"] = pd.to_datetime(dfx["fecha"], errors="coerce")

    # 1) Ventas por mes
    dfx["mes"] = dfx["fecha"].dt.to_period("M").astype(str)
    ventas_mes = dfx.groupby("mes", as_index=False)["importe"].sum().sort_values("mes")

    path1 = out_dir / "ventas_por_mes.png"
    plt.figure()
    plt.plot(ventas_mes["mes"], ventas_mes["importe"], marker="o")
    plt.title("Ventas por mes")
    plt.xlabel("Mes")
    plt.ylabel("Importe")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path1, dpi=200)
    plt.close()
    charts["ventas_por_mes"] = str(path1)

    # 2) Ventas por categoría (Top 10)
    ventas_cat = (
        dfx.groupby("categoria", as_index=False)["importe"].sum()
        .sort_values("importe", ascending=False)
        .head(10)
    )

    path2 = out_dir / "ventas_por_categoria.png"
    plt.figure()
    plt.bar(ventas_cat["categoria"], ventas_cat["importe"])
    plt.title("Ventas por categoría (Top 10)")
    plt.xlabel("Categoría")
    plt.ylabel("Importe")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path2, dpi=200)
    plt.close()
    charts["ventas_por_categoria"] = str(path2)

    # 3) Top productos (Top 10)
    top_prod = (
        dfx.groupby("producto", as_index=False)["importe"].sum()
        .sort_values("importe", ascending=False)
        .head(10)
    )

    path3 = out_dir / "top_productos.png"
    plt.figure()
    plt.bar(top_prod["producto"], top_prod["importe"])
    plt.title("Top 10 productos por ventas")
    plt.xlabel("Producto")
    plt.ylabel("Importe")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path3, dpi=200)
    plt.close()
    charts["top_productos"] = str(path3)

    return charts