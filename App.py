import streamlit as st

# Configurazione della pagina e tema visivo
st.set_page_config(
    page_title="SaaS Preventivi Pro",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stile CSS personalizzato per un look moderno e professionale
st.markdown("""
    <style>
    .main {
        background-color: #F8FAFC;
    }
    .stMetric {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #0F172A;
    }
    </style>
""", unsafe_allow_html=True)

# --- HOME / DASHBOARD ---
st.title("💼 Benvenuto nel tuo Gestionale Pro")
st.write("Gestisci i tuoi documenti commerciali, i clienti e monitora il tuo business in un unico posto.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Preventivi Emessi (Mese)", value="12", delta="+3")
with col2:
    st.metric(label="Fatturato Potenziale", value="€ 14.250", delta="+12%")
with col3:
    st.metric(label="Clienti Attivi", value="8", delta="+1")

st.divider()

st.subheader("🚀 Come iniziare")
st.info("Usa il menu a barra laterale a sinistra per navigare tra le sezioni:\n"
          "- **1_Generatore_Preventivi**: Crea e scarica preventivi in PDF professionali.\n"
          "- **2_Rubrica_Clienti**: Salva e gestisci i dati dei tuoi clienti.")