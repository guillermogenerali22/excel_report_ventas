import pandas as pd
import re


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def _to_float_series(s: pd.Series) -> pd.Series:
    def parse_one(x):
        if pd.isna(x):
            return None
        t = str(x).strip()
        t = t.replace("€", "").replace(" ", "")

        # Si tiene coma, asumimos formato español: 1.234,56 -> 1234.56
        if "," in t:
            t = t.replace(".", "")
            t = t.replace(",", ".")
        else:
            # Si solo hay puntos, asumimos decimal inglés: 60.00 -> 60.00
            # pero si hay más de un punto, los anteriores suelen ser miles: 1.234.567 -> 1234567
            if t.count(".") > 1:
                parts = t.split(".")
                t = "".join(parts[:-1]) + "." + parts[-1]

        # Dejar solo números, signo y punto
        t = re.sub(r"[^0-9\.\-]", "", t)
        try:
            return float(t)
        except:
            return None

    return s.apply(parse_one)
def clean_sales(df_raw: pd.DataFrame):
    df = _normalize_columns(df_raw)

    # Ajusta estos nombres según tu excel real:
    required = ["fecha", "cliente", "producto", "categoria", "unidades", "precio_unitario"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}. Columnas detectadas: {list(df.columns)}")

    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce", dayfirst=True)
    df["unidades"] = pd.to_numeric(df["unidades"], errors="coerce")
    df["precio_unitario"] = _to_float_series(df["precio_unitario"])

    # limpieza de texto
    for c in ["cliente", "producto", "categoria"]:
        df[c] = df[c].astype(str).str.strip()
    df["categoria"] = df["categoria"].str.lower()

    # quitar filas inválidas
    df = df.dropna(subset=["fecha", "unidades", "precio_unitario"])
    df = df[df["unidades"] > 0]
    df = df[df["precio_unitario"] >= 0]

    # duplicados (ajusta el subset si tu excel tiene id de pedido)
    df = df.drop_duplicates(subset=["fecha", "cliente", "producto", "unidades", "precio_unitario"])

    df["importe"] = df["unidades"] * df["precio_unitario"]

    # métricas
    total_ventas = float(df["importe"].sum())
    total_unidades = float(df["unidades"].sum())
    num_pedidos = int(len(df))
    ticket_medio = total_ventas / num_pedidos if num_pedidos else 0.0

    top_productos = (
        df.groupby("producto", as_index=False)["importe"].sum()
        .sort_values("importe", ascending=False)
        .head(10)
    )
    top_clientes = (
        df.groupby("cliente", as_index=False)["importe"].sum()
        .sort_values("importe", ascending=False)
        .head(10)
    )
    por_categoria = (
        df.groupby("categoria", as_index=False)["importe"].sum()
        .sort_values("importe", ascending=False)
    )

    stats = {
        "total_ventas": total_ventas,
        "total_unidades": total_unidades,
        "num_pedidos": num_pedidos,
        "ticket_medio": ticket_medio,
        "top_productos": top_productos,
        "top_clientes": top_clientes,
        "por_categoria": por_categoria,
        "rango_fechas": (df["fecha"].min(), df["fecha"].max()),
    }

    return df, stats