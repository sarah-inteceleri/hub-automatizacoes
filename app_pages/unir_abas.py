"""
Página de Unir Abas - Processamento de Olimpíadas e Paralimpíadas
"""

import streamlit as st
import pandas as pd
from utils.data_processor import OlimpiadasProcessor
from utils.file_handler import FileHandler

def run():
    """Função principal da página de unir abas"""
    
    st.title("📊 Processador de Olimpíadas e Paralimpíadas")
    
    st.markdown("""
    Este sistema processa planilhas de participantes de olimpíadas escolares, 
    separando automaticamente os dados em **Olimpíadas** e **Paralimpíadas**.
    """)
    
    # Informações sobre o critério (no conteúdo principal)
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(
            "**🎯 Olimpíadas**\n\n"
            "Alunos com texto exato:\n"
            "'Não possui deficiência/transtorno'"
        )
    
    with col2:
        st.info(
            "**🥈 Paralimpíadas**\n\n"
            "Qualquer outro valor ou vazio"
        )
    
    st.markdown("---")
    
    # Seção de upload
    render_upload_section()
    
    # Processar arquivo se enviado
    if 'uploaded_file_olimpiadas' in st.session_state and st.session_state['uploaded_file_olimpiadas'] is not None:
        uploaded_file = st.session_state['uploaded_file_olimpiadas']
        
        try:
            with st.spinner("🔄 Processando planilha..."):
                processor = OlimpiadasProcessor()
                file_handler = FileHandler()
                workbook_data = file_handler.read_excel(uploaded_file)
                olimpiadas_df, paralimpiadas_df, anos_ordenados = processor.process_workbook(workbook_data)
                
                st.session_state['olimpiadas'] = olimpiadas_df
                st.session_state['paralimpiadas'] = paralimpiadas_df
                st.session_state['anos_ordenados'] = anos_ordenados
                st.session_state['processed'] = True
                
            st.success("✅ Planilha processada com sucesso!")
            render_results_section(olimpiadas_df, paralimpiadas_df, anos_ordenados, file_handler)
            
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {str(e)}")
            with st.expander("🔍 Ver detalhes do erro"):
                st.exception(e)
    else:
        render_instructions()


def render_upload_section():
    """Renderiza a seção de upload"""
    st.markdown("### 📤 Upload da Planilha")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.file_uploader(
            "Escolha o arquivo Excel",
            type=['xlsx', 'xls'],
            help="Selecione a planilha com múltiplas abas (uma por escola)",
            key='uploaded_file_olimpiadas'
        )


def render_results_section(olimpiadas_df, paralimpiadas_df, anos_ordenados, file_handler):
    """Renderiza a seção de resultados"""
    st.markdown("---")
    st.markdown("## 📊 Resultados")
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    
    total_olimpiadas = olimpiadas_df.iloc[:, 1:].sum().sum() if not olimpiadas_df.empty and len(olimpiadas_df.columns) > 1 else 0
    total_paralimpiadas = paralimpiadas_df['Quantidade'].sum() if not paralimpiadas_df.empty else 0
    total_escolas = len(olimpiadas_df) if not olimpiadas_df.empty else 0
    
    with col1:
        st.metric("🥇 Total Olimpíadas", int(total_olimpiadas))
    with col2:
        st.metric("🥈 Total Paralimpíadas", int(total_paralimpiadas))
    with col3:
        st.metric("🏫 Total de Escolas", total_escolas)
    
    st.markdown("---")
    
    # Olimpíadas
    st.markdown("### 🥇 Olimpíadas - Formato Pivotado")
    
    with st.expander("👁️ Visualizar dados", expanded=True):
        st.dataframe(olimpiadas_df, use_container_width=True, height=400)
    
    col1, col2 = st.columns(2)
    with col1:
        excel_data, mime, ext = file_handler.get_download_button_data(olimpiadas_df, 'excel')
        st.download_button(
            label="📥 Baixar Excel",
            data=excel_data,
            file_name=f"olimpiadas.{ext}",
            mime=mime,
            use_container_width=True
        )
    with col2:
        csv_data, mime, ext = file_handler.get_download_button_data(olimpiadas_df, 'csv')
        st.download_button(
            label="📥 Baixar CSV",
            data=csv_data,
            file_name=f"olimpiadas.{ext}",
            mime=mime,
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Paralimpíadas
    st.markdown("### 🥈 Paralimpíadas - Formato Normalizado")
    
    with st.expander("👁️ Visualizar dados", expanded=True):
        st.dataframe(paralimpiadas_df, use_container_width=True, height=400)
    
    col1, col2 = st.columns(2)
    with col1:
        excel_data, mime, ext = file_handler.get_download_button_data(paralimpiadas_df, 'excel')
        st.download_button(
            label="📥 Baixar Excel",
            data=excel_data,
            file_name=f"paralimpiadas.{ext}",
            mime=mime,
            use_container_width=True
        )
    with col2:
        csv_data, mime, ext = file_handler.get_download_button_data(paralimpiadas_df, 'csv')
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
        - Planilha com múltiplas abas
        - Cada aba = uma escola
        - Aba "DIVISÃO" será ignorada
        
        ### 2️⃣ Estrutura
        - **Linha 1:** Nome da escola
        - **Linha 2:** Cabeçalhos
        - **Linha 3+:** Dados dos alunos
        """)
    
    with col2:
        st.markdown("""
        ### 3️⃣ Processamento
        - ✅ Lê todas as abas
        - ✅ Identifica colunas automaticamente
        - ✅ Separa Olimpíadas/Paralimpíadas
        - ✅ Gera dois relatórios
        """)
    
    st.markdown("---")
    
    # Exemplos
    st.markdown("### 📊 Exemplos de Saída")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🥇 Olimpíadas (Pivotado)**")
        exemplo_olimpiadas = pd.DataFrame({
            'Escola': ['ESC. MUNICIPAL PEIXE-BOI', 'ESC. ESTADUAL EXEMPLO'],
            '1° ano': [5, 3],
            '2° ano': [3, 2],
            '5° ano': [10, 7]
        })
        st.dataframe(exemplo_olimpiadas, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**🥈 Paralimpíadas (Normalizado)**")
        exemplo_paralimpiadas = pd.DataFrame({
            'Escola': ['ESC. MUN. PEIXE-BOI', 'ESC. MUN. PEIXE-BOI'],
            'Categoria': ['TEA', 'TDAH'],
            'Ano': ['5°', '3°'],
            'Quantidade': [10, 5]
        })
        st.dataframe(exemplo_paralimpiadas, use_container_width=True, hide_index=True)