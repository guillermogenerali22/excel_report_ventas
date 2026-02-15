from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def build_pdf_report(df, stats, out_path: str):
    c = canvas.Canvas(out_path, pagesize=A4)
    width, height = A4

    # Título
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 60, "Informe automático de ventas")

    # Resumen
    c.setFont("Helvetica", 12)
    y = height - 100
    min_f, max_f = stats["rango_fechas"]
    c.drawString(50, y, f"Rango de fechas: {min_f.date()} - {max_f.date()}"); y -= 18
    c.drawString(50, y, f"Pedidos: {stats['num_pedidos']}"); y -= 18
    c.drawString(50, y, f"Unidades: {stats['total_unidades']:.0f}"); y -= 18
    c.drawString(50, y, f"Ventas totales: {stats['total_ventas']:.2f} €"); y -= 18
    c.drawString(50, y, f"Ticket medio: {stats['ticket_medio']:.2f} €"); y -= 30

    # Top productos (simple, como lista)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Top 10 productos"); y -= 20
    c.setFont("Helvetica", 11)
    for _, row in stats["top_productos"].iterrows():
        c.drawString(55, y, f"- {row['producto']}: {row['importe']:.2f} €")
        y -= 14
        if y < 80:
            c.showPage()
            y = height - 60

    # Top clientes
    y -= 10
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Top 10 clientes"); y -= 20
    c.setFont("Helvetica", 11)
    for _, row in stats["top_clientes"].iterrows():
        c.drawString(55, y, f"- {row['cliente']}: {row['importe']:.2f} €")
        y -= 14
        if y < 80:
            c.showPage()
            y = height - 60

    c.save()