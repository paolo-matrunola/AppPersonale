import streamlit as st

st.set_page_config(page_title="La mia Web App", page_icon="🚀")

st.title("Benvenuto nella mia prima Web App! 🚀")
st.write("Questa applicazione è scritta interamente in Python.")

# Un piccolo elemento interattivo
nome = st.text_input("Inserisci il tuo nome:")

if nome:
    st.success(f"Ciao {nome}! L'app funziona perfettamente.")