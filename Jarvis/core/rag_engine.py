from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from config.config import MODEL_LLM, LLM_TEMPERATURE, RETRIEVER_K

def get_llm():
    return ChatOllama(
        model=MODEL_LLM, 
        temperature=LLM_TEMPERATURE,
        #Puerto local en el que corre ollama
        base_url="http://127.0.0.1:11434"
    )

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K})

    #Prompt para el LLM, con reglas y conceptos
    system_prompt = (
        "Eres un tutor pedagógico de Ingeniería en Sistemas e IA.\n"
        "Tu objetivo es guiar al estudiante de forma clara y directa en sus dudas sobre el temario.\n\n"
        "REGLAS DE RESPUESTA:\n"
        "1. Si el estudiante te hace una repregunta o aclaración sobre lo que acaban de hablar "
        "(ej. '¿pero si no hay tokens no genera nada?', '¿entonces es como un motor de búsqueda?'), "
        "responde de forma natural (ej. 'Efectivamente...', 'No exactamente...', 'Sí, así es...') "
        "razonando sobre el contexto del temario y el historial.\n"
        "2. Mantén la fidelidad al temario. Si la pregunta busca información de un tema completamente "
        "ajeno que NO está en el texto ni en la conversación previa, responde estrictamente: "
        "'Ese tema o término no está dentro del temario subido.'\n\n"
        "Contexto del temario disponible:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    rag_chain = (
        {
            "context": lambda x: format_docs(retriever.invoke(x["input"])),
            "chat_history": lambda x: x["chat_history"],
            "input": lambda x: x["input"]
        }
        | prompt
        | get_llm()
        | StrOutputParser()
    )
    
    return rag_chain, retriever