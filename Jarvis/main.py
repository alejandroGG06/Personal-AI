import streamlit as st
from ui.sidebar import render_sidebar
from ui.chat import render_chat
from core.document_loader import load_existing_vectorstore

st.set_page_config(
    page_title="Jarvis Tutor IA",
    page_icon="🎓",
    layout="wide"
)

# Cargar base vectorial existente al iniciar la app
if "vectorstore" not in st.session_state:
    existing_store = load_existing_vectorstore()
    if existing_store:
        st.session_state["vectorstore"] = existing_store

def main():
    render_sidebar()
    render_chat()

if __name__ == "__main__":
    main()