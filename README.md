# 📊 Excel Report Ventas (Python)

Herramienta en Python para **limpiar datos de ventas “sucios” desde Excel** y generar automáticamente:

- ✅ `ventas_limpias.csv` (datos normalizados)
- ✅ `informe_ventas.pdf` (resumen con métricas y rankings)

Pensado para negocios que trabajan con Excels desordenados (ventas, pedidos, clientes, stock…) y necesitan un informe en **1 click**.

---

## ✨ Qué hace

### Limpieza automática
- Normaliza nombres de columnas
- Convierte fechas a formato estándar
- Convierte precios con formatos españoles (`45,50`, `1.234,56`, `45,50 €`)
- Elimina duplicados
- Filtra filas inválidas (sin fecha, unidades <= 0, etc.)
- Calcula `importe = unidades * precio_unitario`

### Informe PDF
Incluye:
- Total ventas, total unidades, número de pedidos, ticket medio
- Top productos
- Top clientes

---

## 🧱 Estructura del proyecto
