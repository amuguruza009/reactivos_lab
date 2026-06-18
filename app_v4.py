import streamlit as st
import pandas as pd
import unicodedata

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="Inventario Lab", layout="wide")

# =====================
# NORMALIZACIÓN
# =====================
def normalizar(texto):
    texto = str(texto).lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))

# =====================
# CARGA
# =====================
@st.cache_data
def cargar():
    df = pd.read_excel("reactivos_lab.xlsx", engine="openpyxl")
    df["Sustancia_norm"] = df["Sustancia"].apply(normalizar)
    return df

df = cargar()

# =====================
# UI
# =====================
st.title("🧪 Inventario de Reactivos")

texto = st.text_input("🔎 Buscar reactivo:")

# =====================
# FILTRO
# =====================
if texto:
    texto_norm = normalizar(texto)
    df_filtrado = df[df["Sustancia_norm"].str.contains(texto_norm, na=False)]
else:
    df_filtrado = df

# =====================
# SUGERENCIAS (AUTOCOMPLETE SIMULADO)
# =====================
if texto:
    st.caption("💡 Sugerencias:")
    st.write(list(df_filtrado["Sustancia"].dropna().unique()[:10]))

# =====================
# SELECCIÓN ESTABLE (tipo click seguro)
# =====================
st.subheader("📋 Inventario")

opcion = st.selectbox(
    "Selecciona un reactivo para ver ficha:",
    [""] + list(df_filtrado["Sustancia"].dropna().unique())
)

# =====================
# FICHA
# =====================
if opcion:
    ficha = df[df["Sustancia"] == opcion].iloc[0]

    st.subheader("🧬 Ficha del reactivo")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Sustancia")
        st.write(ficha["Sustancia"])

    with col2:
        for col in df.columns:
            if col not in ["Sustancia", "Sustancia_norm"]:
                st.write(f"**{col}**: {ficha[col]}")

else:
    st.info("Selecciona un reactivo para ver su ficha")
