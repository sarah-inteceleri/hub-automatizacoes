"""
Página de Criação de Etiquetas
"""

import streamlit as st
from modules.etiquetas_nao_adaptadas_logic import interface_nao_adaptadas
from modules.etiquetas_adaptadas_logic import interface_adaptadas

def run():
    """Função principal da página de etiquetas"""
    
    st.title("🏷️ Criação de Etiquetas de Provas")
    
    st.markdown("""
    Esta ferramenta gera etiquetas em PDF para provas escolares, 
    adaptadas ou não adaptadas, a partir de planilhas.
    """)
    
    st.info(
        "⚠️ **Importante:** Os dados de quantitativo de alunos devem estar formatados como números. "
        "No Google Planilhas: **Formatar → Número → Formato de número personalizado**."
    )
    
    st.markdown("---")
    
    # SELETOR DO TIPO DE ETIQUETA (dentro do conteúdo principal)
    st.markdown("### ⚙️ Escolha o Tipo de Etiqueta")
    
    tipo_etiqueta = st.radio(
        "Selecione o tipo de prova:",
        ["📄 Provas Não Adaptadas", "♿ Provas Adaptadas"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Renderizar interface baseada na seleção
    if tipo_etiqueta == "📄 Provas Não Adaptadas":
        st.markdown("### 📄 Etiquetas para Provas Não Adaptadas")
        st.caption("*Para alunos sem necessidades especiais de adaptação*")
        st.markdown("---")
        interface_nao_adaptadas()
        
    else:  # Provas Adaptadas
        st.markdown("### ♿ Etiquetas para Provas Adaptadas")
        st.caption("*Para alunos com deficiências ou transtornos que necessitam de adaptações*")
        st.markdown("---")
        interface_adaptadas()