import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rubrica Clienti", page_icon="👥", layout="wide")

st.title("👥 Gestione Clienti")
st.write("Aggiungi e tieni traccia dei contatti dei tuoi clienti.")

if 'clienti_db' not in st.session_state:
    st.session_state.clienti_db = pd.DataFrame([
        {"Nome Azienda": "Cliente Rossi S.r.l.", "Referente": "Mario Rossi", "Email": "mario@rossi.it", "Telefono": "3331234567"}
    ])

# Modulo di inserimento nuovo cliente
with st.form("nuovo_cliente"):
    st.subheader("Aggiungi un nuovo cliente")
    c1, c2 = st.columns(2)
    with c1:
        nc_nome = st.text_input("Nome Azienda / Cliente")
        nc_rif = st.text_input("Persona Referente")
    with c2:
        nc_email = st.text_input("Email")
        nc_tel = st.text_input("Telefono")
    
    submit = st.form_submit_button("Salva Cliente")
    if submit and nc_nome:
        nuova_riga = pd.DataFrame([{"Nome Azienda": nc_nome, "Referente": nc_rif, "Email": nc_email, "Telefono": nc_tel}])
        st.session_state.clienti_db = pd.concat([st.session_state.clienti_db, nuova_riga], ignore_index=True)
        st.success(f"Cliente '{nc_nome}' aggiunto con successo!")

st.divider()
st.subheader("Elenco Clienti Salvati")
st.dataframe(st.session_state.clienti_db, use_container_width=True)