import streamlit as st
from core.document_loader import process_and_index_files

def render_sidebar():
    """Renderiza el panel lateral para la carga de archivos."""
    with st.sidebar: 
        st.subheader("📚 Documentos")
        uploaded_files = st.file_uploader(
            "Sube tus apuntes (PDF o TXT)", 
            type=["pdf", "txt"], 
            accept_multiple_files=True
        )
        
        if st.button("Añadir Documentos", use_container_width=True):
            if uploaded_files:
                with st.spinner("Procesando e indexando documentos localmente..."):
                    vectorstore = process_and_index_files(uploaded_files)
                    st.session_state["vectorstore"] = vectorstore
                    st.success("¡Documentos indexados correctamente!")
            else:
                st.warning("Por favor, sube al menos un archivo antes de indexar.")