import streamlit as st
import pandas as pd
import unicodedata
import os

st.set_page_config(page_title="Inventario Lab", layout="wide")

def normalizar(texto):
    texto = str(texto).lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))

@st.cache_data(ttl=10)
def cargar_datos():
    df = pd.read_excel("reactivos_lab.xlsx", engine="openpyxl")
    df["Sustancia_norm"] = df["Sustancia"].apply(normalizar)
    return df

df = cargar_datos()

imagenes_grupo = {
    "1":"imagenes/grupo1.jpg",
    "2":"imagenes/grupo2.jpg",
    "3":"imagenes/grupo3.jpg",
    "4":"imagenes/grupo4.jpg",
    "5":"imagenes/grupo5.jpg",
    "7A":"imagenes/grupo7A.jpg",
    "7B":"imagenes/grupo7B.jpg",
    "7C":"imagenes/grupo7C.jpg",
}

tab1, tab2 = st.tabs(["📋 Inventario","🧬 Ficha del reactivo"])

with tab1:
    st.title("📋 Inventario de Reactivos")
    texto = st.text_input("🔎 Buscar reactivo", key="busqueda_tab1")

    if texto:
        texto_norm = normalizar(texto)
        df_filtrado = df[df["Sustancia_norm"].str.contains(texto_norm, na=False)]
    else:
        df_filtrado = df

    if texto:
        st.caption("💡 Sugerencias")
        st.write(list(df_filtrado["Sustancia"].dropna().unique()[:10]))

    st.dataframe(
        df_filtrado.drop(columns=["Sustancia_norm"]),
        use_container_width=True,
        height=500
    )

with tab2:
    st.title("🧬 Ficha del reactivo")

    texto2 = st.text_input(
        "🔎 Buscar para ver ficha",
        key="busqueda_tab2"
    )

    if texto2:

        texto_norm2 = normalizar(texto2)

        resultados = df[df["Sustancia_norm"].str.contains(texto_norm2, na=False)]

        if len(resultados) > 0:

            ficha = resultados.iloc[0]

            col_info, col_img = st.columns([2,1])

            with col_info:

                st.markdown(f"## {ficha['Sustancia']}")

                codigo = ficha["Codigo"]
                if pd.isna(codigo) or codigo == "":
                    codigo = "-"

                c1, c2 = st.columns([1,3])

                with c1:
                    st.markdown("**Código**")

                with c2:
                    st.markdown(
                        f"<div style='font-size:28px'>{codigo}</div>",
                        unsafe_allow_html=True
                    )

                st.divider()

                for col in df.columns:

                    if col in ["Sustancia","Codigo","Sustancia_norm"]:
                        continue

                    valor = ficha[col]

                    if pd.isna(valor) or valor == "":
                        valor = "-"

                    st.markdown(f"**{col}:** {valor}")

            with col_img:

                st.subheader("📍 Ubicación")

                grupo = ficha["Grupo"]

                try:
                    grupo = str(int(float(grupo)))
                except:
                    grupo = str(grupo).strip()

                ruta = imagenes_grupo.get(grupo)

                if ruta and os.path.exists(ruta):

                    st.image(
                        ruta,
                        caption=f"Grupo {grupo}",
                        use_container_width=True
                    )

                elif ruta:

                    st.warning(f"No se encuentra la imagen:\n{ruta}")

                else:

                    st.warning(f"No hay imagen asociada al grupo {grupo}")

        else:

            st.warning("No se ha encontrado ningún reactivo.")

    else:

        st.info("Escribe un reactivo para ver su ficha.")


