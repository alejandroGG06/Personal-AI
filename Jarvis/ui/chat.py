import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from core.rag_engine import get_rag_chain

def render_chat():
    st.title("JARVIS")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "¡Hola! Sube tus apuntes en el panel lateral para empezar a estudiar."}
        ]

    # Renderizado del UI
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Entrada del humano
    if prompt := st.chat_input("Escribe tu pregunta o repregunta..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if "vectorstore" in st.session_state and st.session_state["vectorstore"]:
                rag_chain, retriever = get_rag_chain(st.session_state["vectorstore"])

                with st.spinner("Pensando..."):
                    chat_history = []
                    for m in st.session_state.messages[:-1]: 
                        if m["role"] == "user":
                            chat_history.append(HumanMessage(content=m["content"]))
                        elif m["role"] == "assistant":
                            chat_history.append(AIMessage(content=m["content"]))

                    
                    docs = retriever.invoke(prompt)
                    answer = rag_chain.invoke({
                        "input": prompt,
                        "chat_history": chat_history
                    })

                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                    with st.expander("Ver fuentes"):
                        for i, doc in enumerate(docs):
                            st.write(f"**Fuente {i+1}:** {doc.metadata.get('source', 'Documento')}")
                            st.caption(f"\"{doc.page_content[:200]}...\"")
            else:
                msg_error = "Por favor sube e indexa un documento en la barra lateral antes de consultar."
                st.error(msg_error)
                st.session_state.messages.append({"role": "assistant", "content": msg_error})