import pandas as pd
from pathlib import Path
from charts import generate_charts

from config import INPUT_FILE, OUTPUT_CSV, OUTPUT_PDF, SHEET_NAME
from cleaning import clean_sales
from report_pdf import build_pdf_report


def _resolve_from_project_root(p) -> Path:
    """Make paths work even if PyCharm runs with working dir = src/."""
    project_root = Path(__file__).resolve().parents[1]  # <root>/src/main.py -> <root>
    p = Path(p)  # supports str or Path
    return p if p.is_absolute() else (project_root / p)


def main():
    input_path = _resolve_from_project_root(INPUT_FILE)
    out_csv = _resolve_from_project_root(OUTPUT_CSV)
    out_pdf = _resolve_from_project_root(OUTPUT_PDF)

    # Ensure output folder exists
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    print("Directorio actual:", Path().resolve())
    print("Leyendo Excel:", input_path)

    df_raw = pd.read_excel(input_path, sheet_name=SHEET_NAME)
    df_clean, stats = clean_sales(df_raw)

    df_clean.to_csv(out_csv, index=False, encoding="utf-8-sig")
    build_pdf_report(df_clean, stats, str(out_pdf))

    charts = generate_charts(df_clean, "outputs/charts")
    print("Gráficos generados:", charts)

    print("OK ✅ Generado:", out_csv, "y", out_pdf)


if __name__ == "__main__":
    main()