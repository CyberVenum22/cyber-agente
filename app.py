import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="CyberVenum Agent", page_icon="🛡️")
st.title("🛡️ CyberVenum Intelligence Hub")

# 2. Configuração da API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Configure a GEMINI_API_KEY nos Secrets do Streamlit!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. Inicialização do Modelo (Configuração da Persona)
generation_config = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Você é um Especialista Sênior em Cibersegurança e Hacker Ético. Responda de forma técnica, direta e honesta."
)

# 4. Histórico do Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Lógica do Chat
if prompt := st.chat_input("Solicitar análise de segurança..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Envia o histórico completo para manter o contexto
            chat_session = model.start_chat(history=[])
            response = chat_session.send_message(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                st.error("Limite de cota atingido. Aguarde 30 segundos.")
            elif "404" in error_msg:
                st.error("Erro 404: O Google ainda está ativando sua chave nova. Aguarde 5 minutos.")
            else:
                st.error(f"Erro na API: {error_msg}")
