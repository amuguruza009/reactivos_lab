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
# CARGA DE DATOS
# =====================
@st.cache_data
def cargar_datos():
    df = pd.read_excel("reactivos_lab.xlsx", engine="openpyxl")
    df["Sustancia_norm"] = df["Sustancia"].apply(normalizar)
    return df

df = cargar_datos()

# =====================
# TABS
# =====================
tab1, tab2 = st.tabs(["📋 Inventario", "🧬 Ficha del reactivo"])

# ==========================================================
# TAB 1: INVENTARIO
# ==========================================================
with tab1:
    st.title("📋 Inventario de Reactivos")

    texto = st.text_input("🔎 Buscar reactivo", key="busqueda_tab1")

    # Filtrado
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
# TAB 2: FICHA
# ==========================================================
with tab2:
    st.title("🧬 Ficha del reactivo")

    texto2 = st.text_input("🔎 Buscar para ver ficha", key="busqueda_tab2")

    if texto2:
        texto_norm2 = normalizar(texto2)
        resultados = df[df["Sustancia_norm"].str.contains(texto_norm2, na=False)]

        if len(resultados) > 0:
            ficha = resultados.iloc[0]

            # =====================
            # TÍTULO
            # =====================
            st.markdown(f"## {ficha['Sustancia']}")

            # =====================
            # CÓDIGO ALINEADO
            # =====================
            codigo = ficha.get("Codigo", "-")
            if pd.isna(codigo) or codigo == "":
                codigo = "-"

            col1, col2 = st.columns([1, 3], vertical_alignment="center")

            with col1:
                st.markdown("**Código**")

            with col2:
                st.markdown(
                    f"<div style='font-size:28px; line-height:1.2;'>{codigo}</div>",
                    unsafe_allow_html=True
                )

            st.divider()

            # =====================
            # RESTO DE CAMPOS
            # =====================
            for col in df.columns:
                if col not in ["Sustancia", "Sustancia_norm", "Codigo"]:

                    valor = ficha[col]

                    if pd.isna(valor) or valor == "":
                        valor = "-"

                    st.markdown(f"**{col}:** {valor}")

        else:
            st.warning("No encontrado")

    else:
        st.info("Escribe un reactivo para ver su ficha")
