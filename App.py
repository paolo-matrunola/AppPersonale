import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Generatore Preventivi Pro", page_icon="📄", layout="wide")

# Funzione per generare il PDF in memoria
def genera_pdf(emittente, cliente, df_servizi, note, totale_imponibile, calcolo_iva, totale_finale):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    # Titolo
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, leading=24, textColor=colors.HexColor("#1E3A8A"))
    story.append(Paragraph("PREVENTIVO", title_style))
    story.append(Spacer(1, 12))

    # Info Emittente e Cliente
    info_data = [
        [Paragraph(f"<b>Da:</b><br/>{emittente.replace('\n', '<br/>')}", styles['Normal']),
         Paragraph(f"<b>A:</b><br/>{cliente.replace('\n', '<br/>')}", styles['Normal'])]
    ]
    t_info = Table(info_data, colWidths=[270, 270])
    t_info.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_info)
    story.append(Spacer(1, 20))

    # Tabella Servizi
    table_data = [["Descrizione", "Qtà", "Prezzo Unitario (€)", "Totale (€)"]]
    for _, row in df_servizi.iterrows():
        table_data.append([
            str(row["Descrizione"]),
            str(row["Quantità"]),
            f"{row['Prezzo Unitario (€)']:.2f}",
            f"{row['Totale (€)']:.2f}"
        ])

    t_servizi = Table(table_data, colWidths=[260, 60, 110, 110])
    t_servizi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_servizi)
    story.append(Spacer(1, 15))

    # Totali
    totali_text = f"<b>Imponibile:</b> €{totale_imponibile:.2f}<br/>"
    totali_text += f"<b>IVA:</b> €{calcolo_iva:.2f}<br/>" if calcolo_iva > 0 else "<b>IVA:</b> Regime Forfettario (0%)<br/>"
    totali_text += f"<font size=12 color='#1E3A8A'><b>TOTALE PREVENTIVO: €{totale_finale:.2f}</b></font>"
    
    p_totali = Paragraph(totali_text, ParagraphStyle('TotStyle', parent=styles['Normal'], alignment=2, leading=16))
    story.append(p_totali)

    if note:
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"<b>Note e Condizioni:</b><br/>{note}", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --- INTERFACCIA STREAMLIT ---
st.title("📄 Generatore di Preventivi Professionali")
st.write("Crea preventivi in PDF pronti da inviare ai tuoi clienti in meno di un minuto.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. I tuoi dati (Emittente)")
    emittente = st.text_area("Intestazione Tua / Azienda", "La Mia Azienda S.r.l.\nP.IVA: 12345678901\nEmail: info@azienda.it", height=100)

with col2:
    st.subheader("2. Dati del Cliente")
    cliente = st.text_area("Intestazione Cliente", "Cliente Rossi S.r.l.\nVia Roma 10, Milano\nCod. Fiscale: RSSLNZ80A01H501Z", height=100)

st.subheader("3. Dettaglio Servizi / Prodotti")

# Inizializza tabella dinamica nello stato della sessione
if 'servizi' not in st.session_state:
    st.session_state.servizi = pd.DataFrame([
        {"Descrizione": "Sviluppo Sito Web / App", "Quantità": 1, "Prezzo Unitario (€)": 800.0},
        {"Descrizione": "Consulenza e Configurazione", "Quantità": 2, "Prezzo Unitario (€)": 50.0}
    ])

df_edited = st.data_editor(
    st.session_state.servizi,
    num_rows="dynamic",
    column_config={
        "Quantità": st.column_config.NumberColumn(min_value=1, step=1),
        "Prezzo Unitario (€)": st.column_config.NumberColumn(format="%.2f €")
    },
    use_container_width=True
)

# Calcoli matematici
df_edited["Totale (€)"] = df_edited["Quantità"] * df_edited["Prezzo Unitario (€)"]
totale_imponibile = df_edited["Totale (€)"].sum()

st.subheader("4. Tassazione e Totali")
col_iva, col_tot = st.columns(2)

with col_iva:
    aliquota_iva = st.selectbox("Aliquota IVA (%)", [0, 4, 10, 22], index=3)
    note = st.text_area("Note / Termini di Pagamento", "Pagamento 50% all'ordine, 50% a consegna lavoro. Validità preventivo: 30 giorni.")

calcolo_iva = totale_imponibile * (aliquota_iva / 100)
totale_finale = totale_imponibile + calcolo_iva

with col_tot:
    st.metric("Imponibile", f"€ {totale_imponibile:.2f}")
    st.metric("IVA", f"€ {calcolo_iva:.2f}")
    st.metric("TOTALE FINALE", f"€ {totale_finale:.2f}")

st.divider()

# Generazione e download PDF
pdf_buffer = genera_pdf(emittente, cliente, df_edited, note, totale_imponibile, calcolo_iva, totale_finale)

st.download_button(
    label="📥 Scarica Preventivo in PDF",
    data=pdf_buffer,
    file_name="Preventivo.pdf",
    mime="application/pdf",
    use_container_width=True
)