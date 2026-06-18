import streamlit as st
import pandas as pd
import unicodedata

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="Inventario Lab", layout="wide")

# =====================
# FUNCIONES
# =====================
def normalizar(texto):
    texto = str(texto).lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))

# =====================
# CARGA DATOS
# =====================
@st.cache_data
def cargar_datos():
    df = pd.read_excel("reactivos_lab.xlsx", engine="openpyxl")
    df["Sustancia_norm"] = df["Sustancia"].apply(normalizar)
    return df

df = cargar_datos()

# =====================
# UI
# =====================
st.title("🧪 Inventario de Reactivos de Laboratorio")

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
# TABLA PRINCIPAL
# =====================
st.subheader("📋 Resultados")

st.dataframe(
    df_filtrado.drop(columns=["Sustancia_norm"]),
    use_container_width=True,
    height=400
)

# =====================
# FICHA DETALLADA
# =====================
st.subheader("🧬 Ficha del reactivo")

opcion = st.selectbox(
    "Selecciona un reactivo para ver detalles:",
    [""] + list(df_filtrado["Sustancia"].dropna().unique())
)

if opcion:
    ficha = df[df["Sustancia"] == opcion].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Sustancia")
        st.write(ficha["Sustancia"])

        if "Fórmula" in df.columns:
            st.write("### Fórmula")
            st.write(ficha["Fórmula"])

    with col2:
        for col in df.columns:
            if col not in ["Sustancia", "Sustancia_norm"]:
                st.write(f"**{col}**: {ficha[col]}")
