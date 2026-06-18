import streamlit as st
import pandas as pd
import unicodedata

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Inventario Lab", layout="wide")

# =========================
# NORMALIZACIÓN
# =========================
def normalizar(texto):
    texto = str(texto).lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))

# =========================
# CARGA DATOS
# =========================
@st.cache_data
def cargar_datos():
    df = pd.read_excel("reactivos_lab.xlsx", engine="openpyxl")
    df["Sustancia_norm"] = df["Sustancia"].apply(normalizar)
    return df

df = cargar_datos()

# =========================
# UI
# =========================
st.title("🧪 Inventario de Reactivos de Laboratorio")

texto = st.text_input("🔎 Buscar reactivo:")

# =========================
# FILTRADO
# =========================
if texto:
    texto_norm = normalizar(texto)
    df_filtrado = df[df["Sustancia_norm"].str.contains(texto_norm, na=False)]
else:
    df_filtrado = df

# =========================
# SUGERENCIAS (pseudo-autocomplete)
# =========================
if texto:
    sugerencias = df_filtrado["Sustancia"].dropna().unique()
    st.caption("💡 Sugerencias:")
    st.write(list(sugerencias[:10]))

# =========================
# SELECCIÓN TIPO “CLICK”
# =========================
st.subheader("📋 Inventario (haz click en un reactivo)")

event = st.dataframe(
    df_filtrado.drop(columns=["Sustancia_norm"]),
    use_container_width=True,
    height=400,
    on_select="rerun",
    selection_mode="single-row"
)

# =========================
# OBTENER FILA SELECCIONADA
# =========================
if event.selection.rows:
    idx = event.selection.rows[0]
    ficha = df_filtrado.iloc[idx]

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
