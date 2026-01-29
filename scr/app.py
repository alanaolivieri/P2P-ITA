import streamlit as st
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title = "Revisiones P2P",
    layout = "wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "data" / "p2p_latest.xlsx"

df = pd.read_excel(DATA_PATH)

st.title("📊 Estado para revisiones P2P")

st.info(
    "**Solo las personas marcadas con ✅ pueden realizar el P2P.**\n\n"
    "Si no estás habilitado/a, pero sabes que tienes aprobado el sprint, contacta con tu mentor."
)

st.sidebar.header("🔎 Filtros")

solo_habilitados = st.sidebar.checkbox(
    "Mostrar solo habilitados para P2P",
    value=True
)

if "Mentor" in df.columns:
    mentores = st.sidebar.multiselect(
        "Filtrar por mentor",
        options=df["Mentor"].unique(),
        default=df["Mentor"].unique()
    )
    df = df[df["Mentor"].isin(mentores)]

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.caption("IT Academy · Sistema de revisión P2P")
