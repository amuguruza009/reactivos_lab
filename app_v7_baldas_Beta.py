import streamlit as st
import pandas as pd
import unicodedata

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="Inventario Lab CAD", layout="wide")

# =====================
# NORMALIZACIÓN
# =====================
def normalizar(texto):
    texto = str(texto).lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))

# =====================
# DECODIFICAR UBICACIÓN DESDE CÓDIGO
# =====================
def decode_location(codigo):
    codigo = str(codigo)

    if "." in codigo:
        balda, pos = codigo.split(".")
    else:
        balda, pos = codigo, "0"

    if pos in ["1", "A", "L"]:
        zona = "izquierda"
    elif pos in ["2", "B"]:
        zona = "centro"
    else:
        zona = "derecha"

    return balda, zona

# =====================
# CARGA DE DATOS
# =====================
@st.cache_data(ttl=10)
def cargar_datos():
    df = pd.read_excel("reactivos_lab.xlsx", engine="openpyxl")
    df["Sustancia_norm"] = df["Sustancia"].apply(normalizar)

    # 🔥 añadir ubicación derivada
    df["Balda"], df["Zona"] = zip(*df["Codigo"].apply(decode_location))

    return df

df = cargar_datos()

# =====================
# ESTADO GLOBAL
# =====================
if "zona_sel" not in st.session_state:
    st.session_state.zona_sel = None

if "codigo_sel" not in st.session_state:
    st.session_state.codigo_sel = None

# =====================
# TABS
# =====================
tab1, tab2 = st.tabs(["📋 Inventario", "🗺️ Mapa laboratorio CAD + Ficha"])

# ==========================================================
# TAB 1: INVENTARIO
# ==========================================================
with tab1:
    st.title("📋 Inventario de Reactivos")

    texto = st.text_input("🔎 Buscar reactivo")

    if texto:
        texto_norm = normalizar(texto)
        df_filtrado = df[df["Sustancia_norm"].str.contains(texto_norm, na=False)]
    else:
        df_filtrado = df

    if texto:
        st.caption("💡 Sugerencias:")
        st.write(list(df_filtrado["Sustancia"].dropna().unique()[:10]))

    st.dataframe(df_filtrado.drop(columns=["Sustancia_norm"]))

    # 🔁 búsqueda inversa por tabla
    st.subheader("🔁 Búsqueda por ubicación")

    col1, col2 = st.columns(2)

    with col1:
        balda = st.selectbox("Balda", sorted(df["Balda"].unique()))

    with col2:
        zona = st.selectbox("Zona", ["izquierda", "centro", "derecha"])

    filtrados = df[(df["Balda"] == balda) & (df["Zona"] == zona)]

    st.dataframe(filtrados)

# ==========================================================
# TAB 2: MAPA CAD + FICHA
# ==========================================================
with tab2:
    st.title("🗺️ Mapa tipo laboratorio (CAD simplificado)")

    # =====================
    # MAPA VISUAL
    # =====================
    baldas = sorted(df["Balda"].unique())

    for b in baldas:

        st.markdown(f"### 🔬 Balda {b}")

        cols = st.columns(3)

        zonas = ["izquierda", "centro", "derecha"]

        for i, z in enumerate(zonas):

            count = len(df[(df["Balda"] == b) & (df["Zona"] == z)])

            label = f"{z} ({count})"

            if cols[i].button(label, key=f"{b}_{z}"):

                st.session_state.zona_sel = (b, z)

    st.divider()

    # =====================
    # RESULTADO SELECCIÓN
    # =====================
    if st.session_state.zona_sel:

        b, z = st.session_state.zona_sel

        st.success(f"📍 Zona seleccionada: Balda {b} - {z}")

        seleccion = df[(df["Balda"] == b) & (df["Zona"] == z)]

        st.dataframe(seleccion)

        # =====================
        # FICHA SI SELECCIONAS UNO
        # =====================
        st.subheader("🧬 Selecciona reactivo")

        opciones = seleccion["Sustancia"].tolist()

        if opciones:

            elegido = st.selectbox("Reactivo", opciones)

            ficha = seleccion[seleccion["Sustancia"] == elegido].iloc[0]

            st.markdown(f"## {ficha['Sustancia']}")

            # código grande
            st.markdown(f"### Código: {ficha['Codigo']}")

            st.markdown(f"**Balda:** {ficha['Balda']}")
            st.markdown(f"**Zona:** {ficha['Zona']}")

            for col in df.columns:
                if col not in ["Sustancia", "Sustancia_norm", "Codigo", "Balda", "Zona"]:
                    val = ficha[col]
                    if pd.isna(val) or val == "":
                        val = "-"
                    st.markdown(f"**{col}:** {val}")

    else:
        st.info("Selecciona una zona del mapa para explorar el laboratorio")
