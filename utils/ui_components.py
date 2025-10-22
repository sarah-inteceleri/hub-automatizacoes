# utils/ui_components.py
"""
Componentes de interface do usuário para Streamlit
"""

import streamlit as st
import pandas as pd
from typing import List
from utils.file_handler import FileHandler


def render_header():
    """Renderiza o cabeçalho da aplicação"""
    col1, col2 = st.columns([1, 8])
    with col1:
        st.markdown("# 🏅")
    with col2:
        st.title("Processador de Olimpíadas e Paralimpíadas")
    
    st.markdown("---")


def render_upload_section():
    """Renderiza a seção de upload de arquivo"""
    st.markdown("### 📤 Upload da Planilha")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        uploaded_file = st.file_uploader(
            "Escolha o arquivo Excel",
            type=['xlsx', 'xls'],
            help="Selecione a planilha com múltiplas abas (uma por escola)"
        )
    
    return uploaded_file


def render_results_section(
    olimpiadas_df: pd.DataFrame,
    paralimpiadas_df: pd.DataFrame,
    anos_ordenados: List[str],
    file_handler: FileHandler
):
    """Renderiza a seção de resultados"""
    st.markdown("---")
    st.markdown("## 📊 Resultados")
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    
    # Calcular totais - ajustado para nova estrutura
    total_olimpiadas = 0
    if not olimpiadas_df.empty and len(olimpiadas_df.columns) > 1:
        # Soma todas as colunas exceto 'Escola'
        total_olimpiadas = olimpiadas_df.iloc[:, 1:].sum().sum()
    
    total_paralimpiadas = paralimpiadas_df['Quantidade'].sum() if not paralimpiadas_df.empty else 0
    total_escolas = len(olimpiadas_df) if not olimpiadas_df.empty else 0
    
    with col1:
        st.metric("🥇 Total Olimpíadas", int(total_olimpiadas))
    with col2:
        st.metric("🥈 Total Paralimpíadas", int(total_paralimpiadas))
    with col3:
        st.metric("🏫 Total de Escolas", total_escolas)
    
    st.markdown("---")
    
    # Seção Olimpíadas
    st.markdown("### 🥇 Olimpíadas - Formato Pivotado")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📊 **{len(olimpiadas_df)}** escolas processadas")
    with col2:
        st.info(f"📅 **{len(anos_ordenados)}** anos escolares encontrados")
    
    # Preview
    with st.expander("👁️ Visualizar dados", expanded=True):
        st.dataframe(
            olimpiadas_df,
            use_container_width=True,
            height=400
        )
    
    # Botões de download
    col1, col2 = st.columns(2)
    
    with col1:
        excel_data, mime, ext = file_handler.get_download_button_data(
            olimpiadas_df, 'excel'
        )
        st.download_button(
            label="📥 Baixar Excel",
            data=excel_data,
            file_name=f"olimpiadas.{ext}",
            mime=mime,
            use_container_width=True
        )
    
    with col2:
        csv_data, mime, ext = file_handler.get_download_button_data(
            olimpiadas_df, 'csv'
        )
        st.download_button(
            label="📥 Baixar CSV",
            data=csv_data,
            file_name=f"olimpiadas.{ext}",
            mime=mime,
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Seção Paralimpíadas
    st.markdown("### 🥈 Paralimpíadas - Formato Normalizado")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📊 **{len(paralimpiadas_df)}** registros processados")
    with col2:
        if not paralimpiadas_df.empty:
            escolas_para = paralimpiadas_df['Escola'].nunique()
            st.info(f"🏫 **{escolas_para}** escolas com participantes")
    
    # Preview
    with st.expander("👁️ Visualizar dados", expanded=True):
        st.dataframe(
            paralimpiadas_df,
            use_container_width=True,
            height=400
        )
    
    # Botões de download
    col1, col2 = st.columns(2)
    
    with col1:
        excel_data, mime, ext = file_handler.get_download_button_data(
            paralimpiadas_df, 'excel'
        )
        st.download_button(
            label="📥 Baixar Excel",
            data=excel_data,
            file_name=f"paralimpiadas.{ext}",
            mime=mime,
            use_container_width=True
        )
    
    with col2:
        csv_data, mime, ext = file_handler.get_download_button_data(
            paralimpiadas_df, 'csv'
        )
        st.download_button(
            label="📥 Baixar CSV",
            data=csv_data,
            file_name=f"paralimpiadas.{ext}",
            mime=mime,
            use_container_width=True
        )


def render_instructions():
    """Renderiza as instruções de uso"""
    st.markdown("---")
    st.markdown("## 📋 Como Usar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 1️⃣ Preparação
        - Certifique-se de que sua planilha tenha múltiplas abas
        - Cada aba representa uma escola diferente
        - A aba "DIVISÃO" será automaticamente ignorada
        
        ### 2️⃣ Estrutura Esperada
        - **Linha 1:** Nome da escola
        - **Linha 2:** Cabeçalhos das colunas
        - **Linha 3+:** Dados dos estudantes
        
        ### 3️⃣ Colunas Necessárias
        - `Ano` - Ano escolar do estudante
        - `Deficiência/Transtorno` - Status do estudante
        """)
    
    with col2:
        st.markdown("""
        ### 4️⃣ Processamento
        O sistema irá:
        - ✅ Ler todas as abas (exceto "DIVISÃO")
        - ✅ Identificar automaticamente as colunas
        - ✅ Separar em Olimpíadas e Paralimpíadas
        - ✅ Gerar dois relatórios diferentes
        
        ### 5️⃣ Formatos de Saída
        **🥇 Olimpíadas:** Formato pivotado
        - Anos regulares primeiro, EJA/EJAI no final
        
        **🥈 Paralimpíadas:** Formato normalizado
        - Ano sem a palavra "ano" (ex: "1°", "2°")
        """)
    
    st.markdown("---")
    
    # Exemplo visual
    st.markdown("### 📊 Exemplo de Saída")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🥇 Olimpíadas (Formato Pivotado)**")
        st.markdown("""
        **Estrutura:** `Escola | 1° ano | 2° ano | ... | EJA | EJAI`
        
        **Anos regulares em ordem crescente, EJA/EJAI no final**
        """)
        exemplo_olimpiadas = pd.DataFrame({
            'Escola': ['ESCOLA MUNICIPAL PEIXE-BOI', 'ESCOLA ESTADUAL EXEMPLO'],
            '1° ano': [5, 3],
            '2° ano': [3, 2],
            '5° ano': [10, 7],
            'EJA': [2, 4],
            'EJAI': [1, 2]
        })
        st.dataframe(exemplo_olimpiadas, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**🥈 Paralimpíadas (Formato Normalizado)**")
        st.markdown("""
        **Colunas:** `Escola | Categoria | Ano | Quantidade`
        
        **Ano aparece apenas como "1°", "2°", "3°", etc.**
        """)
        exemplo_paralimpiadas = pd.DataFrame({
            'Escola': ['ESCOLA MUNICIPAL PEIXE-BOI', 'ESCOLA MUNICIPAL PEIXE-BOI', 'ESCOLA MUNICIPAL PEIXE-BOI'],
            'Categoria': ['TEA', 'TDAH', 'Dislexia'],
            'Ano': ['5°', '3°', '1°'],
            'Quantidade': [10, 5, 3]
        })
        st.dataframe(exemplo_paralimpiadas, use_container_width=True, hide_index=True)