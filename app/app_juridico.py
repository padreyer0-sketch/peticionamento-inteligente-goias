import streamlit as st
from groq import Groq
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Vade Mecum IA - Pedro Afonso", page_icon="⚖️", layout="wide")

# --- LÓGICA DE BUSCA MULTI-LEIS ---
def buscar_contexto_inteligente(pergunta):
    # Pasta onde as leis ficam (Saindo da pasta 'app' e indo para 'biblioteca_juridica')
    diretorio_leis = os.path.join("..", "biblioteca_juridica")
    
    # Mapeamento inicial
    arquivo_alvo = "CTE_Goias.txt" # Padrão
    pergunta_up = pergunta.upper()
    
    if any(w in pergunta_up for w in ["CONSTITUIÇÃO", "CF", "FEDERAL"]): arquivo_alvo = "Constituicao_Federal.txt"
    elif any(w in pergunta_up for w in ["CIVIL", "CONTRATO"]): arquivo_alvo = "Codigo_Civil.txt"
    elif any(w in pergunta_up for w in ["PENAL", "CRIME"]): arquivo_alvo = "Codigo_Penal.txt"
    elif any(w in pergunta_up for w in ["TRABALHO", "CLT"]): arquivo_alvo = "CLT.txt"

    caminho_final = os.path.join(diretorio_leis, arquivo_alvo)
    
    # Se o arquivo não existir, busca o que estiver disponível
    if not os.path.exists(caminho_final):
        return "Aguardando download das leis via Raspador...", "Nenhum"

    with open(caminho_final, "r", encoding="utf-8") as f:
        conteudo = f.read()
    
    # Pega um trecho de 30k caracteres
    return conteudo[:30000], arquivo_alvo

# --- INTERFACE ---
st.title("⚖️ Sistema de Peticionamento Inteligente")

with st.sidebar:
    st.header("Configurações")
    chave_api = st.text_input("Sua Chave Groq:", type="password")

pergunta_usuario = st.text_area("Descreva o caso ou peça a fundamentação:", height=200)

if st.button("GERAR FUNDAMENTAÇÃO"):
    if not chave_api:
        st.error("Insira a chave do Groq!")
    else:
        with st.spinner("Analisando..."):
            trecho, nome_lei = buscar_contexto_inteligente(pergunta_usuario)
            client = Groq(api_key=chave_api)
            
            prompt = f"Você é um Advogado Sênior. Fundamente o caso abaixo usando este trecho de lei ({nome_lei}):\n{trecho}\n\nCaso: {pergunta_usuario}"
            
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.2
            )
            st.markdown(f"### 📄 Fundamentação (Base: {nome_lei})")
            st.success(completion.choices[0].message.content)