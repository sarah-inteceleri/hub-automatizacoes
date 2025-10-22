"""
Hub Central de Automatizações
Sistema unificado com múltiplas ferramentas
"""

import streamlit as st

# Configuração da página (ÚNICA no projeto)
st.set_page_config(
    page_title="Hub de Automatizações",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #4F46E5;
    }
    </style>
""", unsafe_allow_html=True)

# Importar páginas
from pages import etiquetas
from pages import unir_abas

def main():
    """Função principal do hub"""
    
    # Sidebar - Menu de navegação
    with st.sidebar:
        st.markdown("# 🛠️ Automatizações")
        st.markdown("---")
        
        pagina_selecionada = st.radio(
            "Escolha a ferramenta:",
            ["🏠 Início", "🏷️ Criação de Etiquetas", "📊 Unir Abas (Olimpíadas)"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.info("💡 Selecione uma ferramenta acima")
    
    # Conteúdo principal
    if pagina_selecionada == "🏠 Início":
        render_home()
    elif pagina_selecionada == "🏷️ Criação de Etiquetas":
        etiquetas.run()
    elif pagina_selecionada == "📊 Unir Abas (Olimpíadas)":
        unir_abas.run()

def render_home():
    """Renderiza a página inicial"""
    
    st.markdown('<div class="main-header">🛠️ Hub de Automatizações Educacionais</div>', unsafe_allow_html=True)
    
    st.markdown("## Bem-vindo! 👋")
    st.markdown("### Use o menu lateral para escolher uma ferramenta")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏷️ Criação de Etiquetas
        
        **Funcionalidades:**
        - ✅ Etiquetas para provas **adaptadas**
        - ✅ Etiquetas para provas **não adaptadas**
        - ✅ Detecção automática de colunas
        - ✅ Limpeza inteligente de nomes
        - ✅ Exportação em PDF
        
        **Formatos aceitos:** CSV, Excel (XLSX)
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Unir Abas (Olimpíadas)
        
        **Funcionalidades:**
        - ✅ Consolida múltiplas abas
        - ✅ Separa Olimpíadas e Paralimpíadas
        - ✅ Formato pivotado (Olimpíadas)
        - ✅ Formato normalizado (Paralimpíadas)
        - ✅ Exportação em Excel ou CSV
        
        **Formatos aceitos:** Excel (XLSX, XLS)
        """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🛠️ Ferramentas", "2")
    with col2:
        st.metric("📄 Formatos", "5+")
    with col3:
        st.metric("⚡ Automação", "100%")

if __name__ == "__main__":
    main()