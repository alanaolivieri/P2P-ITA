import streamlit as st
import pandas as pd
import os
import datetime
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title = "Organización Data Analytics",
    layout = "wide"
)

if "mostrar_infografia" not in st.session_state:
    st.session_state.mostrar_infografia = False

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "data" / "p2p_latest.xlsx"
ORG_PATH = BASE_DIR.parent / "data" / "actividades.xlsx"
INFOGRAFIA_PATH = BASE_DIR.parent / "data" / "infografia.jpg"


st.sidebar.header("📌 Navegación")
vista = st.sidebar.radio("Ir a", ["P2P", "Organización"])

st.sidebar.divider()

st.sidebar.header("🔎 Filtros")

if vista == "P2P":
    df = pd.read_excel(DATA_PATH)

    st.title("📊 Estado para revisiones P2P")

    st.info(
        "**Solo las personas marcadas con ✅ pueden realizar el P2P.**\n\n"
        "Si no estás habilitado/a, pero sabes que tienes aprobado el sprint, contacta con tu mentor."
    )

    solo_habilitados = st.sidebar.checkbox(
        "Mostrar solo habilitados para P2P",
        value=True
    )

    if solo_habilitados and "✅" in df.columns:
        df = df[df["✅"] == True]

    if "Mentor" in df.columns:
        mentores = st.sidebar.multiselect(
            "Filtrar por mentor",
            options=df["Mentor"].dropna().unique(),
            default=df["Mentor"].dropna().unique()
        )
        df = df[df["Mentor"].isin(mentores)]

    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption("IT Academy · Sistema de revisión P2P")

else:
    st.title("🗓️ Organización de actividades")
    if INFOGRAFIA_PATH.exists():
        col1, col2 = st.columns([1, 5])

        with col1:
            st.image(str(INFOGRAFIA_PATH), width=180)

            if st.button("Ampliar imagen"):
                st.session_state.mostrar_infografia = True

        if st.session_state.mostrar_infografia:
            st.divider()
            st.subheader("Infografía ampliada")

            st.image(str(INFOGRAFIA_PATH), use_container_width=True)

            if st.button("Cerrar imagen"):
                st.session_state.mostrar_infografia = False
                st.rerun()
    else:
        st.warning("No se encontró la infografía.")

    df_org = pd.read_excel(ORG_PATH)

    if "Comentari" in df_org.columns:
        df_org = df_org.drop(columns=["Comentari"])

    if "Data" in df_org.columns:
        df_org["Data"] = pd.to_datetime(df_org["Data"], errors="coerce").dt.normalize()

        hoy = datetime.date.today()
        fin_30 = hoy + datetime.timedelta(days=30)

        min_fecha = df_org["Data"].min().date()
        max_fecha = df_org["Data"].max().date()

        valor_inicio = max(hoy, min_fecha)
        valor_fin = min(fin_30, max_fecha)

        rango_fechas = st.sidebar.date_input(
            "Filtrar por fecha",
            value=(valor_inicio, valor_fin),
            min_value=min_fecha,
            max_value=max_fecha
        )

        if len(rango_fechas) == 2:
            inicio, fin = rango_fechas
        else:
            inicio, fin = valor_inicio, valor_fin

        df_org = df_org[
            df_org["Data"].between(pd.Timestamp(inicio), pd.Timestamp(fin))
        ]

        df_org["Data"] = df_org["Data"].dt.strftime("%d-%m")

    if "Session" in df_org.columns:
        df_org["Session"] = df_org["Session"].astype(str).str.replace("\n", "<br>", regex=False)

    html = df_org.to_html(index=False, escape=False, justify="center")

    st.markdown(
        """
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th {
            text-align: center !important;
        }
        td {
            vertical-align: top;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(html, unsafe_allow_html=True)
