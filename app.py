import streamlit as st
import pandas as pd
import unicodedata

# --- Cargar datos ---
ruta = reactivos_lab.xlsx
df = pd.read_excel(ruta)

# --- normalización ---
def normalizar(texto):
    texto = str(texto).lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))

df["Sustancia_norm"] = df["Sustancia"].apply(normalizar)

# --- UI ---
st.title("Buscador de Reactivos")

texto = st.text_input("Buscar reactivo:")

# --- lógica ---
if texto == "":
    st.dataframe(df, use_container_width=True)
else:
    texto_norm = normalizar(texto)
    resultado = df[df["Sustancia_norm"].str.contains(texto_norm, na=False)]
    st.dataframe(resultado, use_container_width=True)
