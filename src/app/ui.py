from __future__ import annotations
import os
import streamlit as st

# Mapeo limpio y definitivo alineado con la barra lateral estilizada
PAGE_LINKS = [
    ("Inicio", "main.py", "🏠"),
    ("MRU", "pages/mru.py", "📊"),
    ("MRUA", "pages/mrua.py", "🚀"),
    ("Historial", "pages/historial.py", "🗄️"),
]

def get_api_base_url() -> str:
    return os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")

def get_experiments_url() -> str:
    return f"{get_api_base_url()}/experiments"

def apply_theme() -> None:
    pass

def render_topbar(active_page: str) -> None:
    st.sidebar.title("🧪 PhysiLab")
    st.sidebar.caption(f"Página actual: {active_page}")
    st.sidebar.markdown("---")
    for label, page_path, icon in PAGE_LINKS:
        st.sidebar.page_link(page_path, label=f"{icon} {label}")
    st.sidebar.markdown("---")
    st.sidebar.info("💡 Proyecto Fullstack")

def render_hero(title: str, subtitle: str, tag: str | None = None) -> None:
    st.title(title)
    if tag:
        st.caption(tag)
    st.write(subtitle)
    st.markdown("---")