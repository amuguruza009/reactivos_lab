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
# CARGA DATOS
# =====================
@st.cache_data
def cargar():
    df = pd.read_excel("reactivos_lab.xlsx", engine="openpyxl")
    df["Sustancia_norm"] = df["Sustancia"].apply(normalizar)
    return df

df = cargar()

# =====================
# TABS
# =====================
tab1, tab2 = st.tabs(["📋 Inventario", "🧬 Fichas de reactivo"])

# ==========================================================
# TAB 1 → INVENTARIO (tabla + búsqueda)
# ==========================================================
with tab1:
    st.title("📋 Inventario de reactivos")

    texto = st.text_input("🔎 Buscar reactivo", key="busqueda_tab1")

    if texto:
        texto_norm = normalizar(texto)
        df_filtrado = df[df["Sustancia_norm"].str.contains(texto_norm, na=False)]
    else:
        df_filtrado = df

    # Sugerencias (pseudo-autocomplete)
    if texto:
        st.caption("💡 Sugerencias:")
        st.write(list(df_filtrado["Sustancia"].dropna().unique()[:10]))

    st.dataframe(
        df_filtrado.drop(columns=["Sustancia_norm"]),
        use_container_width=True,
        height=500
    )

# ==========================================================
# TAB 2 → FICHAS (buscador + detalle)
# ==========================================================
with tab2:
    st.title("🧬 Ficha del reactivo")

    texto2 = st.text_input("🔎 Buscar para ver ficha", key="busqueda_tab2")

    if texto2:
        texto_norm2 = normalizar(texto2)
        resultados = df[df["Sustancia_norm"].str.contains(texto_norm2, na=False)]

        if len(resultados) > 0:
            ficha = resultados.iloc[0]

            st.subheader(f"🧪 {ficha['Sustancia']}")

            col1, col2 = st.columns(2)

            with col1:
                for col in df.columns:
                    if col not in ["Sustancia", "Sustancia_norm"]:
                        st.write(f"**{col}**: {ficha[col]}")

        else:
            st.warning("No encontrado")
    else:
        st.info("Escribe un reactivo para ver su ficha")
