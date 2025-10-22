"""
Página de Criação de Etiquetas
"""

import streamlit as st
import pandas as pd
from modules.etiquetas_nao_adaptadas_logic import interface_nao_adaptadas
from modules.etiquetas_adaptadas_logic import interface_adaptadas

def run():
    """Função principal da página de etiquetas"""
    
    st.title("🏷️ Criação de Etiquetas de Provas")
    
    st.markdown("""
    Esta ferramenta gera etiquetas em PDF para provas escolares, 
    adaptadas ou não adaptadas, a partir de planilhas.
    """)
    
    st.markdown("---")
    
    # Menu lateral específico desta página
    st.sidebar.markdown("### ⚙️ Configurações de Etiquetas")
    opcao = st.sidebar.radio(
        "Escolha o tipo de etiqueta:", 
        ["Provas Não Adaptadas", "Provas Adaptadas"]
    )

    st.sidebar.markdown("---")
    st.sidebar.info(
        "⚠️ **Importante:** Os dados de quantitativo de alunos "
        "devem estar formatados como números. No Google Planilhas: "
        "**Formatar → Número → Formato de número personalizado**."
    )

    # Renderizar interface baseada na seleção
    if opcao == "Provas Não Adaptadas":
        interface_nao_adaptadas()
    elif opcao == "Provas Adaptadas":
        interface_adaptadas()