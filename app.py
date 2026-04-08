import streamlit as st
import os
from google import genai

# Configuração da Página
st.set_page_config(page_title="CyberVenum Agent", page_icon="🛡️")
st.title("🛡️ CyberVenum Intelligence")

# Pegando a chave das variáveis de ambiente
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Inicializa o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada
if prompt := st.chat_input("Digite seu comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
  # Chamada para o Gemini
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash-002",  # Nome técnico completo
                contents=[prompt],
                config={
                    'system_instruction': "Você é um Especialista Sênior em Cibersegurança. Responda de forma técnica e direta.",
                    'temperature': 0.2
                }
            )
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("O modelo não retornou resposta.")
                
        except Exception as e:
            # Se o erro 404 persistir, tentaremos o modelo 2.0 que é o padrão da lib nova
            st.error(f"Erro na API: {str(e)}")
