"""
Hub Central de Automatizacoes
Sistema unificado com multiplas ferramentas
"""

import streamlit as st

st.set_page_config(
    page_title="Hub de Automatizacoes",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para estilizar
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 16px;
        font-weight: 500;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        background-color: white;
        color: #333;
        margin-bottom: 10px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #f5f5f5;
        border-color: #4F46E5;
        color: #4F46E5;
    }
    .titulo-principal {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f2937;
        margin-top: 150px;
        margin-bottom: 30px;
    }
    .subtitulo {
        font-size: 1.8rem;
        text-align: center;
        color: #6b7280;
        margin-bottom: 80px;
    }
    </style>
""", unsafe_allow_html=True)

# Importar paginas
from app_pages import etiquetas
from app_pages import unir_abas

def main():
    """Funcao principal do hub"""
    
    # Inicializar session state
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = "home"
    
    # SIDEBAR - Menu de navegacao
    with st.sidebar:
        st.markdown("# Menu")
        st.markdown("---")
        
        # Botao Criacao de Etiquetas
        if st.button("Criacao de Etiquetas", use_container_width=True):
            st.session_state.pagina_atual = "etiquetas"
            st.rerun()
        
        # Botao Unir Abas
        if st.button("Unir Abas", use_container_width=True):
            st.session_state.pagina_atual = "unir_abas"
            st.rerun()
        
        st.markdown("---")
        st.caption("💡 Clique em uma opcao acima")
    
    # RENDERIZAR CONTEUDO
    if st.session_state.pagina_atual == "home":
        render_home()
    elif st.session_state.pagina_atual == "etiquetas":
        etiquetas.run()
    elif st.session_state.pagina_atual == "unir_abas":
        unir_abas.run()

def render_home():
    """Tela inicial - antes de escolher qualquer opcao"""
    
    # Titulo principal centralizado
    st.markdown(
        '<div class="titulo-principal">Inteleceleri - Equipe de Projetos</div>', 
        unsafe_allow_html=True
    )
    
    # Subtitulo centralizado
    st.markdown(
        '<div class="subtitulo">Escolha uma opção ao lado e otimize seu tempo</div>', 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()