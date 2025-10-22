"""
Página de Criação de Etiquetas
"""

import streamlit as st
from modules.nao_adaptadas import interface_nao_adaptadas
from modules.adaptadas import interface_adaptadas

def run():
    """Função principal da página de etiquetas"""
    
    st.markdown("# 🏷️ Sistema de Criação de Etiquetas")
    
    st.info(
        "⚠️ **Importante:** Os dados de quantitativo de alunos devem estar formatados como números. "
        "No Google Planilhas: **Formatar → Número → Formato de número personalizado**."
    )
    
    st.markdown("---")
    
    # Abas DENTRO da página de etiquetas
    tab1, tab2 = st.tabs(["📄 Provas Não Adaptadas", "♿ Provas Adaptadas"])
    
    with tab1:
        st.markdown("### 📄 Etiquetas - Provas Não Adaptadas")
        st.markdown("*Para alunos sem necessidades especiais de adaptação*")
        st.markdown("---")
        interface_nao_adaptadas()
    
    with tab2:
        st.markdown("### ♿ Etiquetas - Provas Adaptadas")
        st.markdown("*Para alunos com deficiências ou transtornos que necessitam de adaptações*")
        st.markdown("---")
        interface_adaptadas()