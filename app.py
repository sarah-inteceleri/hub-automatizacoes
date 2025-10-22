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
    .tool-card {
        border: 2px solid #E5E7EB;
        border-radius: 10px;
        padding: 1.5rem;
        background-color: #F9FAFB;
        margin-bottom: 1rem;
    }
    .tool-card h3 {
        color: #4F46E5;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Importar páginas
from pages import etiquetas, unir_abas

def main():
    """Função principal do hub"""
    
    # Cabeçalho principal
    st.markdown('<div class="main-header">🛠️ Hub de Automatizações</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f6e0.png", width=80)
        st.markdown("---")
        st.markdown("### 📂 Ferramentas Disponíveis")
        
        pagina = st.radio(
            "Selecione:",
            ["🏠 Início", "🏷️ Criação de Etiquetas", "📊 Unir Abas (Olimpíadas)"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.info("💡 **Dica:** Selecione uma ferramenta acima para começar")
    
    # Roteamento
    if pagina == "🏠 Início":
        render_home()
    elif pagina == "🏷️ Criação de Etiquetas":
        etiquetas.run()
    elif pagina == "📊 Unir Abas (Olimpíadas)":
        unir_abas.run()

def render_home():
    """Renderiza a página inicial"""
    
    st.markdown("## Bem-vindo ao Hub de Automatizações! 👋")
    st.markdown("### Ferramentas disponíveis:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tool-card">
            <h3>🏷️ Criação de Etiquetas</h3>
            <p><strong>Funcionalidades:</strong></p>
            <ul>
                <li>Gera etiquetas para provas adaptadas e não adaptadas</li>
                <li>Processa planilhas automaticamente</li>
                <li>Detecta colunas de forma inteligente</li>
                <li>Limpa nomes de escolas</li>
                <li>Exporta PDFs prontos para impressão</li>
            </ul>
            <p><strong>Formatos aceitos:</strong> CSV, Excel (XLSX)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tool-card">
            <h3>📊 Unir Abas (Olimpíadas)</h3>
            <p><strong>Funcionalidades:</strong></p>
            <ul>
                <li>Consolida múltiplas abas de planilhas</li>
                <li>Separa Olimpíadas e Paralimpíadas</li>
                <li>Formato pivotado para Olimpíadas</li>
                <li>Formato normalizado para Paralimpíadas</li>
                <li>Exporta em Excel ou CSV</li>
            </ul>
            <p><strong>Formatos aceitos:</strong> Excel (XLSX, XLS)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Instruções gerais
    st.markdown("### 🚀 Como começar:")
    st.markdown("""
    1. **Selecione uma ferramenta** no menu lateral
    2. **Faça upload** do arquivo necessário
    3. **Configure** as opções (se necessário)
    4. **Baixe** os resultados processados
    """)
    
    st.markdown("---")
    
    # Informações adicionais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🛠️ Ferramentas", "2")
    with col2:
        st.metric("📄 Formatos", "5+")
    with col3:
        st.metric("⚡ Automação", "100%")

if __name__ == "__main__":
    main()