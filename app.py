import streamlit as st
import google.generativeai as genai

# 1. DESIGN CYBERPUNK
st.set_page_config(page_title="CYBERVENUM_CORE", page_icon="🛡️")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    h1 { color: #00FF41 !important; text-shadow: 0 0 10px #00FF41; text-transform: uppercase; }
    .stChatMessage { background-color: #050505 !important; border: 1px solid #00FF41 !important; color: #00FF41 !important; }
    .stChatInput input { background-color: #000 !important; border: 1px solid #00FF41 !important; color: #00FF41 !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ CYBERVENUM_INTEL_HUB")

# 2. CONEXÃO COM A IA
if "GEMINI_API_KEY" not in st.secrets:
    st.error("ERRO: CHAVE NÃO ENCONTRADA.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash-latest", # O sufixo -latest força a versão estável
    system_instruction="Você é um Especialista Sênior em Cibersegurança. Responda de forma técnica e direta."
)

# 3. LÓGICA DO CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ESPERANDO COMANDO..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"> {prompt}")

    with st.chat_message("assistant"):
        try:
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.code(f"⚠️ [SYSTEM_FAILURE]: {str(e)}")
