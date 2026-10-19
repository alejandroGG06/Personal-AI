# Personal AI

# Local RAG AI Tutor - Asistente de Estudio con IA Local

Un Tutor Virtual e interactivo basado en arquitectura RAG (Retrieval-Augmented Generation) que corre 100% en local y offline. 

Permite a los estudiantes subir sus propios apuntes o temarios en formato PDF o TXT, indexarlos vectorialmente y realizar consultas o repreguntas conceptuales con respuestas precisas, contextualizadas y sin alucinaciones.

---

## Características Principales

 100% Privado y Local: Ejecución totalmente offline utilizando Ollama y ChromaDB. Ningún dato sale de tu equipo.

 Indexación Dinámica (RAG): Carga archivos PDF o TXT, fragmenta el texto mediante *RecursiveCharacterTextSplitter* y genera *embeddings* vectoriales al instante.

 Historial Conversacional Múltiple: Interfaz tipo ChatGPT que permite crear nuevos chats, guardar conversaciones en el sidebar y mantener el contexto para repreguntas o aclaraciones.

-Transparencia en las Fuentes: Incluye un desplegable interactivo para consultar exactamente qué fragmento y página del documento se utilizó para generar la respuesta.

-Logs en Tiempo Real: Seguimiento detallado en la terminal sobre el progreso de procesamiento y troceado por lotes.

---

##Tecnología Utilizada

* **Frontend / Interfaz:** [Streamlit]
* **Orquestación de IA / RAG:** [LangChain]
* **Modelos Locales (LLM & Embeddings):** [Ollama]
  * **LLM:** `llama3.2:1b`
  * **Embeddings:** `nomic-embed-text`
* **Base de Datos Vectorial:** [ChromaDB]
* **Procesamiento de Documentos:** `PyPDFLoader` y `TextLoader`
