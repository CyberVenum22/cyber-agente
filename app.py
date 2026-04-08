import streamlit as st
import os
from google import genai

# 1. Configuração da Página
st.set_page_config(page_title="CyberVenum Agent", page_icon="🛡️")
st.title("🛡️ CyberVenum Intelligence Hub")

# 2. Inicialização do Cliente
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Configure a GEMINI_API_KEY nos Secrets do Streamlit!")
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Histórico do Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Entrada do Usuário
if prompt := st.chat_input("Solicitar análise de segurança..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Resposta do Agente
    with st.chat_message("assistant"):
        try:
            # Modelo estável para evitar 404 e 429
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[prompt],
                config={
                    'system_instruction': "Você é um Especialista Sênior em Cibersegurança e Hacker Ético. Responda de forma técnica, honesta e direta.",
                    'temperature': 0.1
                }
            )
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("O modelo não retornou resposta (possível bloqueio de segurança).")
                
        except Exception as e:
            st.error(f"Erro Crítico: {str(e)}")
            st.info("Dica: Se aparecer '429', aguarde 30 segundos. Se for '404', a chave ainda está sendo ativada pelo Google.")
